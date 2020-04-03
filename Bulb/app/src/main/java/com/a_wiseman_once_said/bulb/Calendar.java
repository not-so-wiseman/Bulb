package com.a_wiseman_once_said.bulb;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CalendarView;
import android.widget.ListView;

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

public class Calendar extends AppCompatActivity {

    private static JSONObject CALENDAR;

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
                CALENDAR = new JSONObject(result);
            } catch (JSONException e) {
                e.printStackTrace();
            }

        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_calendar);

        Button calendarBtn = (Button) findViewById(R.id.calendarBtn);
        calendarBtn.setBackground(getResources().getDrawable(R.drawable.ic_calendar_icon_disabled));

        CalendarView calendar = (CalendarView) findViewById(R.id.calendarView);


        Calendar.FetchURL getUrl = new Calendar.FetchURL();
        try {
            String endpoint = buildEndPoint("calendar");
            String result = getUrl.execute(endpoint).get();


        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
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

    public void updateEvents(String month) throws JSONException {
        JSONArray events = CALENDAR.getJSONArray(month);

        ListView eventsList = (ListView) findViewById(R.id.events);
        eventsList.setAdapter(arrayAdapter);

        ArrayList<String> monthlyEvenets = new ArrayList<String>();
        for( int i = 0; i < events.length(); i++ ){
            JSONObject aEvent = events.getJSONObject(i);
            String eventName = aEvent.getString("Event")
        }
        ArrayList<String> grades = getStringofGrades();
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_list_item_1, grades);
    }

    public void switchToCalculator(View view) {
        Intent calculatorIntent = new Intent(this, GradesPage.class);
        startActivity(calculatorIntent);
    }
}
