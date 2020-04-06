package com.a_wiseman_once_said.bulb;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ExecutionException;

import javax.net.ssl.HttpsURLConnection;

public class Login extends AppCompatActivity {
    private WebView webView;

    // Fetches a special URL for D2L's login page for Bulb
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
                while (data != -1){
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
            String D2LURL = result.replace("\"", "");

            webView = (WebView) findViewById(R.id.d2lLogin);
            webView.getSettings().setAppCacheEnabled(false);
            webView.getSettings().setJavaScriptEnabled(true);
            webView.setWebViewClient(new WebViewClient(){
                @Override
                public void onPageFinished(WebView view, String url) {
                    super.onPageFinished(view, url);

                    if(url.contains("https://www.blub.tech"))
                    {
                        saveToken(url);
                        openGradesPage();
                    }

                }
            });
            webView.loadUrl(D2LURL);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        FetchURL getUrl = new FetchURL();
        try {
            String d2lURL = getUrl.execute("https://www.blub.tech/auth").get();

        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void saveToken(String token) {
        SharedPreferences sharedPref = this.getSharedPreferences("com.a_wiseman_once_said.bulb", Context.MODE_PRIVATE);
        sharedPref.edit().putString("token", token).apply();
    }

    public void openGradesPage() {
        Intent gradesPageIntent = new Intent(this, GradesPage.class);
        startActivity(gradesPageIntent);
    }
}
