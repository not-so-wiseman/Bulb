/**
 * The Calendar program implements the functionallity for Bulb's calendar page
 *
 * @auther Emily Wiseman & Christian James
 * @version 1.0
 * @since 2020-04-01
 */

package com.a_wiseman_once_said.bulb;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
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
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.concurrent.ExecutionException;

import javax.net.ssl.HttpsURLConnection;

import com.prolificinteractive.materialcalendarview.CalendarDay;
import com.prolificinteractive.materialcalendarview.DayViewDecorator;
import com.prolificinteractive.materialcalendarview.DayViewFacade;
import com.prolificinteractive.materialcalendarview.MaterialCalendarView;
import com.prolificinteractive.materialcalendarview.OnMonthChangedListener;
import com.prolificinteractive.materialcalendarview.spans.DotSpan;

public class Calendar extends AppCompatActivity {

    // Container for JSON collected from www.blub.tech/api/calendar
    private static JSONObject CALENDAR;

    public class FetchURL extends AsyncTask<String, Void, String> {
        /**
         * Fetches JSON from Bulb's API
         * @param urls A url string to send requests to
         */
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

    public class EventDecorator implements DayViewDecorator {
        /**
         * Adds custom decoration to the MaterialCalendarView class so that
         * the calendar displays blue calendars behind event dates.
         */
        private final HashSet<CalendarDay> dates;

        public EventDecorator(Collection<CalendarDay> dates) {
            this.dates = new HashSet<>(dates);
        }

        @Override
        public boolean shouldDecorate(CalendarDay day) {
            return dates.contains(day);
        }

        @Override
        public void decorate(DayViewFacade view) {
            view.setSelectionDrawable(getResources().getDrawable(R.drawable.ic_calendar_empty));
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_calendar);

        // Disables the button for the calendar page
        Button calendarBtn = (Button) findViewById(R.id.calendarBtn);
        calendarBtn.setBackground(getResources().getDrawable(R.drawable.ic_calendar_icon_disabled));
        calendarBtn.setEnabled(false);

        // Initializes the calendar widget
        MaterialCalendarView calendarView = (MaterialCalendarView) findViewById(R.id.calendarView);
        calendarView.setOnMonthChangedListener(new OnMonthChangedListener() {
            @Override
            public void onMonthChanged(MaterialCalendarView widget, CalendarDay date) {
                int month = date.getMonth();
                try {
                    calendarChangeAlert();
                    updateEvents(month, widget);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });


        FetchURL getUrl = new FetchURL();
        try {
            // Grabs JSON from Bulb's API for the first time
            String endpoint = buildEndPoint("calendar");
            String result = getUrl.execute(endpoint).get();
            CALENDAR = new JSONObject(result);

            int currentMonth = CalendarDay.today().getMonth();
            updateEvents(currentMonth, calendarView);
            highlightCurrentDay(calendarView);

        } catch (JSONException | ExecutionException | InterruptedException e) {
            e.printStackTrace();
         }

    }

    public String getToken() {
        /**
         * Gets the token generated by the user when they logged into the app
         * from app storage.
         * @return String The user's authentication token
          */
        SharedPreferences sharedPref = this.getSharedPreferences("com.a_wiseman_once_said.bulb", Context.MODE_PRIVATE);
        String token = sharedPref.getString("token", "");
        token = token.replace("&", "%26");
        return token;
    }

    public String buildEndPoint(String route) {
        /**
         * Builds an endpoint for Bulb's api using the user's token
         * and the api's root.
         * @return String A url for Bulb's api
         */
        String userToken = getToken();
        String endPoint = "https://www.blub.tech/api/";
        endPoint = endPoint.concat(route).concat("?token=").concat(userToken);
        return endPoint;
    }


    public void updateEvents(int month, MaterialCalendarView widget) throws JSONException {
        /**
         * Extracts the JSON data for a given month (determined by 'month') and adds
         * the events for that month to the list of upcoming events and the calendar.
         * @param monthNum A number representing a month of the year
         * @param widget An instance of a calenadr view
         */
        JSONArray events = CALENDAR.getJSONArray(String.valueOf(month));

        // Grabs the list view object shown below "Upcoming Events"
        ListView eventsList = (ListView) findViewById(R.id.events);
        ArrayList<String> monthlyEvents = new ArrayList<String>();

        // Loops through the list of events for a given month
        for( int i = 0; i < events.length(); i++ ){
            JSONObject aEvent = events.getJSONObject(i);
            String eventName = aEvent.getString("Name");
            String eventDayStr = aEvent.getString("Day");
            String eventMonthStr = aEvent.getString("Month");
            String eventYearStr = aEvent.getString("Year");

            monthlyEvents.add(eventName + "\n" + eventMonthStr + " " + eventDayStr);

            // Adds blue calendar decoration the given date on the calendar
            CalendarDay calDay = CalendarDay.from(
                    Integer.parseInt(eventYearStr),
                    month,
                    Integer.parseInt(eventDayStr)
            );
            widget.addDecorator(new EventDecorator(Collections.singleton(calDay)));
        }

        // Converts the list of events so they can be passed to the list view object
        ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_list_item_1, monthlyEvents);
        eventsList.setAdapter(arrayAdapter);
    }

    public void highlightCurrentDay(MaterialCalendarView widget){
        // Highlights the current day of the year pink on the calendar
        CalendarDay calDay = CalendarDay.from(
                CalendarDay.today().getYear(),
                CalendarDay.today().getMonth(),
                CalendarDay.today().getDay()
        );
        widget.setDateSelected(calDay, true);
    }

    public void calendarChangeAlert (){
        Toast.makeText(this, "Refreshed Events", Toast.LENGTH_SHORT).show();
    }

    public void switchToCalculator(View view) {
        /**
         * Navigates to the app's Calculator page
         */
        Intent calculatorIntent = new Intent(this, GradesPage.class);
        startActivity(calculatorIntent);
    }
}
