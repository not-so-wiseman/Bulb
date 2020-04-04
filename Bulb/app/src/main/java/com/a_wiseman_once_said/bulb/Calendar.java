package com.a_wiseman_once_said.bulb;

import androidx.annotation.NonNull;
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
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

import javax.net.ssl.HttpsURLConnection;

public class Calendar extends AppCompatActivity implements CalendarView.OnDateChangeListener{

    private static JSONObject CALENDAR;

    @Override
    public void onSelectedDayChange(@NonNull CalendarView view, int year, int month, int dayOfMonth) {
        try {
            updateEvents(month);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onPointerCaptureChanged(boolean hasCapture) {

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
        setContentView(R.layout.activity_calendar);

        Button calendarBtn = (Button) findViewById(R.id.calendarBtn);
        calendarBtn.setBackground(getResources().getDrawable(R.drawable.ic_calendar_icon_disabled));

        Calendar.FetchURL getUrl = new Calendar.FetchURL();
        try {
            String endpoint = buildEndPoint("calendar");
            String result = getUrl.execute(endpoint).get();
            CALENDAR = new JSONObject(result);
            updateEvents(4);
        } catch (JSONException | ExecutionException | InterruptedException e) {
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

    public void updateEvents(int monthNum) throws JSONException {
        String month = String.valueOf(monthNum);
        JSONArray events = CALENDAR.getJSONArray(month);

        ListView eventsList = (ListView) findViewById(R.id.events);

        ArrayList<String> monthlyEvents = new ArrayList<String>();


        for( int i = 0; i < events.length(); i++ ){
            JSONObject aEvent = events.getJSONObject(i);
            String eventName = aEvent.getString("Name").concat("\n");
            String eventDate = aEvent.getString("Month") + " " + aEvent.getString("Day");
            monthlyEvents.add(eventName + eventDate);
        }

        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_list_item_1, monthlyEvents);
        eventsList.setAdapter(arrayAdapter);

    }

    public void switchToCalculator(View view) {
        Intent calculatorIntent = new Intent(this, GradesPage.class);
        startActivity(calculatorIntent);
    }
}
