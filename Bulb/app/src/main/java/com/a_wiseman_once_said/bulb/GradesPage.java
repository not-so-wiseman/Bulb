package com.a_wiseman_once_said.bulb;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.PopupMenu;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

import javax.net.ssl.HttpsURLConnection;

public class GradesPage extends AppCompatActivity implements PopupMenu.OnMenuItemClickListener, editGradeLogic.EditGradeDialogListener {

    private static JSONObject RESULT_JSON;

    private static JSONObject COURSE;
    private static String COURSE_NAME = "";
    private static String COURSE_AVERAGE = "";
    private static JSONArray COURSE_GRADES;
    private static String GOAL = "You need a 0% in the rest of the course to reach your goal";

    @Override
    public void applyTexts(String goal) throws JSONException {
        getGoal(goal);
        Toast.makeText(this, goal, Toast.LENGTH_SHORT).show();
    }


    // Fetches JSON from Bulb's API
    public class FetchURL extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... urls) {
            String result = "";
            URL url;
            HttpsURLConnection urlConnection = null;

            try {
                url = new URL(urls[0]);
                urlConnection = (HttpsURLConnection) url.openConnection();
                InputStream in = urlConnection.getInputStream();
                InputStreamReader reader = new InputStreamReader(in);

                int data = reader.read();
                while (data != -1) {
                    char current = (char) data;
                    result += current;
                    data = reader.read();
                }

                return result;
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            return null;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_grades_page);

        Button calculatorBtn = (Button) findViewById(R.id.calcBtn);
        calculatorBtn.setBackground(getResources().getDrawable(R.drawable.ic_calculator_icon_disabled));
        calculatorBtn.setEnabled(false);

        Button editBtn = (Button) findViewById(R.id.editBtn);
        editBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                updateGoalMenu(v);
            }
        });

        try {
            getGrades();
            getGoal("50");
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }


    // Dropdown Menu Functions
    @Override
    public boolean onMenuItemClick(MenuItem item) {
        Toast.makeText(this, "Refreshed Page", Toast.LENGTH_SHORT).show();
        return true;
    }

    public void showMenu(View btn) throws JSONException {
        PopupMenu popup = new PopupMenu(this, btn);
        popup.setOnMenuItemClickListener(this);
        popup.inflate(R.menu.courses_selector);

        Menu menuOptions = popup.getMenu();
        JSONArray courses = RESULT_JSON.getJSONArray("CourseData");

        for( int i = 0; i < courses.length(); i++ ) {
            String courseName = courses.getJSONObject(i).getString("Name");
            menuOptions.getItem(i).setTitle(courseName);
            menuOptions.getItem(i).setVisible(true);
        }
        popup.show();
    }

    public void updateGoalMenu(View view) {
        editGradeLogic dialog = new editGradeLogic();
        dialog.show(getSupportFragmentManager(), "edit goals");
    }




    // Auth. functions
    public String getToken() {
        SharedPreferences sharedPref = this.getSharedPreferences("com.a_wiseman_once_said.bulb", Context.MODE_PRIVATE);
        String token = sharedPref.getString("token", "");
        token = token.replace("&", "%26");
        return token;
    }




    // String formatting
    public String buildEndPoint(String route) {
        String userToken = getToken();
        String endPoint = "https://www.blub.tech/api/";
        endPoint = endPoint.concat(route).concat("?token=").concat(userToken);
        return endPoint;
    }

    public ArrayList<String> getStringofGrades() throws JSONException {
        ArrayList<String> grades = new ArrayList<String>();

        for( int i = 0; i < COURSE_GRADES.length(); i++ ){
            JSONObject gradeItem = COURSE_GRADES.getJSONObject(i);
            String name = gradeItem.getString("Name");
            String points = gradeItem.getString("Points");
            String percent = gradeItem.getString("Percent").concat("%");
            grades.add(name + "    " + points + "    " + percent);
        }

        return grades;
    }




    // UI functions
    public void setText(int id, String text){
        TextView textView = (TextView) findViewById(id);
        textView.setText(text);
    }

    public void updateOverallUI() throws JSONException {
        JSONObject overall = RESULT_JSON.getJSONObject("Overall");

        // Updates first two panels
        String overallAverage = overall.getString("Average");
        setText(R.id.average, overallAverage);
        String overallRemaining = overall.getString("Remaining");
        setText(R.id.remaining, overallRemaining);

        String promotion = overall.getString("Promotion");
        String description = "Your average is " + overallAverage + " you need to get a "
                + promotion + " in the remaining course material to make promotion.";
        setText(R.id.description, description);
    }

    public void updateCourseUI() throws JSONException {
        // Set button name
        Button btn = (Button) findViewById(R.id.courseBtn);
        btn.setText(COURSE_NAME);

        // Update progress bar/pie chart
        String gradeString = COURSE_AVERAGE.replace("%", "");
        int progress = Integer.parseInt(gradeString);
        ProgressBar pieChart = (ProgressBar) findViewById(R.id.pie);
        pieChart.setProgress(progress);

        // Update course average
        setText(R.id.courseAverage,COURSE_AVERAGE);

        // Update grades list
        ListView gradeList = (ListView) findViewById(R.id.gradeItems);
        ArrayList<String> grades = getStringofGrades();
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_list_item_1, grades);
        gradeList.setAdapter(arrayAdapter);

        // Update goals description
        setText(R.id.courseInfo,GOAL);
    }




    // HTTP Requests and handling
    public void getGrades() {
        GradesPage.FetchURL getUrl = new GradesPage.FetchURL();
        String endpoint = buildEndPoint("grades-all");

        try {
            String result = getUrl.execute(endpoint).get();

            RESULT_JSON = new JSONObject(result);

            JSONObject currentCourse = RESULT_JSON.getJSONArray("CourseData").optJSONObject(0);
            updateData(currentCourse);

            updateCourseUI();
            updateOverallUI();

        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public void getGoal(String goal) throws JSONException {
        GradesPage.FetchURL getUrl = new GradesPage.FetchURL();

        String selectedCourseId = COURSE.getString("Id");
        String endpoint = buildEndPoint("grades/" + selectedCourseId + "/goal" );
        endpoint += ("&goal=" + goal);

        try {
            String result = getUrl.execute(endpoint).get();

            JSONObject goalResult = new JSONObject(result);
            String gradeToAchieve = goalResult.getString("gradeToAchieve");
            GOAL = "You need a " + gradeToAchieve + "% in the rest of the course to reach your goal";

            updateCourseUI();

        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public void updateData(JSONObject currentCourse) throws JSONException {
        COURSE = currentCourse;
        COURSE_NAME = COURSE.getString("Name");
        COURSE_AVERAGE = COURSE.getJSONArray("Average").getString(0);
        COURSE_GRADES = COURSE.getJSONArray("Grades");
    }






    // Page Navigation functions
    public void switchToCalendar(View view) {
        Intent calendarIntent = new Intent(this, Calendar.class);
        startActivity(calendarIntent);
    }

}
