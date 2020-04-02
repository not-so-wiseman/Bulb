package com.a_wiseman_once_said.bulb;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
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

public class GradesPage extends AppCompatActivity implements PopupMenu.OnMenuItemClickListener {

    private static JSONObject RESULT_JSON;
    private static String GOAL = "50";
    private static String COURSE_NAME = "";
    private static String COURSE_AVERAGE = "";
    private static JSONArray COURSE_GRADES;


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

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);

            try {
                JSONObject gradesData = new JSONObject(result);
                JSONObject overallJSON = gradesData.getJSONObject("Overall");
                setDescription(overallJSON);
                setOverallPanels(overallJSON);


                // gradesJSON.getJSONObject(0);
                //String average = courseData.getString("Average");
                //setText(R.id.average, average);

            } catch (JSONException e) {
                e.printStackTrace();
            }

        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_grades_page);

        GradesPage.FetchURL getUrl = new GradesPage.FetchURL();
        try {
            String endpoint = buildEndPoint("grades-all");
            String result = getUrl.execute(endpoint).get();
            RESULT_JSON = new JSONObject(result);
            JSONObject currentCourse = RESULT_JSON.getJSONArray("CourseData").optJSONObject(0);

            updateData(currentCourse);
            updateUI();

        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        return super.onCreateOptionsMenu(menu);

    }

    @Override
    public boolean onMenuItemClick(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.item1:
                Toast.makeText(this, "Item 1 clicked", Toast.LENGTH_SHORT).show();
                return true;
            case R.id.item2:
                Toast.makeText(this, "Item 2 clicked", Toast.LENGTH_SHORT).show();
                return true;
            default:
                return false;
        }
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


    public void setText(int id, String text){
        TextView textView = (TextView) findViewById(id);
        textView.setText(text);
    }


    public String getToken() {
        SharedPreferences sharedPref = this.getSharedPreferences("com.a_wiseman_once_said.bulb", Context.MODE_PRIVATE);
        String token = sharedPref.getString("token", "");
        token = token.replace("&", "%26");
        return token;
    }

    public String buildEndPoint(String route) {
        String userToken = getToken();
        String endPoint = "https://www.blub.tech/api/";
        endPoint = endPoint.concat(route).concat("?token=").concat(userToken);
        return endPoint;
    }

    public void setDescription(JSONObject overallJSON) throws JSONException {
        String overallAverage = overallJSON.getString("Average");
        String achieve = "40%";
        String average = "Your average is ".concat(overallAverage);
        String goal = " you need to get a ".concat(achieve).concat(
                " in the remaining course material to make promotion.");
        average = average.concat(goal);
        setText(R.id.description, average);
    }

    public void setOverallPanels(JSONObject overallJSON) throws JSONException {
        String overallRemaining = overallJSON.getString("Remaining");
        String overallAverage = overallJSON.getString("Average");
        setText(R.id.average, overallAverage);
        setText(R.id.remaining, overallRemaining);
    }

    public JSONObject filterForCourse(JSONArray courses) {
        return null;
    }

    public ArrayList<String> getStringofGrades() throws JSONException {
        ArrayList<String> grades = new ArrayList<String>();

        for( int i = 0; i < COURSE_GRADES.length(); i++ ){
            JSONObject gradeItem = COURSE_GRADES.getJSONObject(i);
            String name = gradeItem.getString("Name");
            String points = "(".concat(gradeItem.getString("Points")).concat(")");
            String percent = gradeItem.getString("Percent").concat("%");
            grades.add(name.concat("\t\t").concat(points).concat("\t").concat(percent));
        }

        return null;
    }

    public void updateData(JSONObject currentCourse) throws JSONException {
        COURSE_NAME = currentCourse.getString("Name");
        COURSE_AVERAGE = currentCourse.getJSONArray("Average").getString(0);
        COURSE_GRADES = currentCourse.getJSONArray("Grades");
    }

    public void updateUI() {
        // Set button name
        Button btn = (Button) findViewById(R.id.courseBtn);
        btn.setText(COURSE_NAME);

        // Update progress bar/pie chart
        String gradeString = COURSE_AVERAGE.replace("%", "");
        int progress = Integer.parseInt(gradeString);
        ProgressBar pieChart = (ProgressBar) findViewById(R.id.pie);
        pieChart.setProgress(progress);

        // Update course average
        TextView percent = (TextView) findViewById(R.id.courseAverage);
        percent.setText(COURSE_AVERAGE);

        // Update grades list
        ListView grades = (ListView) findViewById(R.id.gradeItems);

    }



}
