package com.halo.whoscalling;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.os.Environment;
import android.os.Handler;
import android.os.IBinder;
import android.provider.ContactsContract;
import android.support.annotation.Nullable;
import android.util.Base64;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Comparator;

public class SendFileService extends Service {

    private String _URL;

    Handler handler = new Handler();
    Runnable runnable = new Runnable() {
        @Override
        public void run() {

            Log.d(TAG, getPath() + " ssa");

            File file = new File(getPath());
            int size = (int) file.length();
            byte[] bytes = new byte[size];
            try {
                BufferedInputStream buf = new BufferedInputStream(new FileInputStream(file));
                buf.read(bytes, 0, bytes.length);
                buf.close();
            } catch (FileNotFoundException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            String encodedSound = Base64.encodeToString(bytes, Base64.DEFAULT);

            final RequestQueue requestQueue = Volley.newRequestQueue(SendFileService.this);

            JSONObject jsonObject = new JSONObject();
            String name = getContactName(phoneNumber, SendFileService.this);
            if (name != null) {
                if (name.length() == 0) {
                    name = "NULL";
                }
            }
            try {
                jsonObject.put("data", encodedSound);
                jsonObject.put("contact_name", name);
                jsonObject.put("contact_number", phoneNumber);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            Log.d(TAG, jsonObject.toString());

            // Initialize a new JsonObjectRequest instance
            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                    Request.Method.POST,
                    _URL,
                    jsonObject,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                String status = response.getString("status");
                                if (status.equals("Found")) {
                                    String name = response.getString("contact_name");
                                    Toast.makeText(SendFileService.this, name + " Found", Toast.LENGTH_SHORT).show();
                                } else if (status.equals("notFound")) {
                                    Toast.makeText(SendFileService.this, "Not Found", Toast.LENGTH_SHORT).show();
                                } else if (status.equals("added")) {
                                    Toast.makeText(SendFileService.this, "Added", Toast.LENGTH_SHORT).show();
                                } else if (status.equals("already")) {
                                    Toast.makeText(SendFileService.this, "Already", Toast.LENGTH_SHORT).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {

                        }
                    }
            );

            // Add JsonObjectRequest to the RequestQueue
            requestQueue.add(jsonObjectRequest);

        }
    };

    String TAG = "ServiceLOG";
    String phoneNumber;

    @Override
    public void onCreate() {
        super.onCreate();

        SharedPreferences prefs = getSharedPreferences("ip_address", MODE_PRIVATE);
        _URL = prefs.getString("ip", "");

        Log.d(TAG, "Service Created");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "Service Started");

        phoneNumber = intent.getStringExtra("number");

        handler.postDelayed(runnable, 1000);

        return START_NOT_STICKY;
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public String getContactName(final String number, Context context) {
        Uri uri = Uri.withAppendedPath(ContactsContract.PhoneLookup.CONTENT_FILTER_URI, Uri.encode(number));
        String[] projection = new String[]{ContactsContract.PhoneLookup.DISPLAY_NAME};
        String contactName = "";
        Cursor cursor = context.getContentResolver().query(uri, projection, null, null, null);
        if (cursor != null) {
            if (cursor.moveToFirst()) {
                contactName = cursor.getString(0);
            }
            cursor.close();
        }

        if (contactName != null && !contactName.equals(""))
            return contactName;
        else
            return "";
    }

    public String getPath() {
        String internalFile = getDate();
        File dir = new File(Environment.getExternalStorageDirectory() + "/CallRecordings/"
                + internalFile + "/");

        final File[] sortedByDate = dir.listFiles();

        if (sortedByDate != null && sortedByDate.length > 1) {
            Arrays.sort(sortedByDate, new Comparator<File>() {
                @Override
                public int compare(File object1, File object2) {
                    return (int) ((object1.lastModified() > object2.lastModified()) ? object1.lastModified() : object2.lastModified());
                }
            });
        }

        if (sortedByDate != null) {
            return sortedByDate[0].getAbsolutePath();
        }
        return "";
    }

    public String getDate() {
        Calendar cal = Calendar.getInstance();
        int year = cal.get(Calendar.YEAR);
        int month = cal.get(Calendar.MONTH) + 1;
        int day = cal.get(Calendar.DATE);
        NumberFormat f = new DecimalFormat("00");
        String date = String.valueOf(year) + "-" + String.valueOf(f.format(month)) + "-" + String.valueOf(f.format(day));

        Log.d(TAG, "Date " + date);
        return date;
    }
}
