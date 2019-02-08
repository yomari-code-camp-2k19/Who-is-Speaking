package com.halo.whoscalling;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.telephony.TelephonyManager;
import android.util.Log;

public class PhoneStateReceiver extends BroadcastReceiver {

    static final String TAG = "PhoneStateeee";
    public static String phoneNumber = "";
    public static String name;

    @Override
    public void onReceive(Context context, Intent intent) {
        try {
            Bundle extras = intent.getExtras();
            String state = extras.getString(TelephonyManager.EXTRA_STATE);

            if (extras != null) {
                if (state.equals(TelephonyManager.EXTRA_STATE_RINGING)) {
                    Log.d(TAG, "Call Ringing");

                } else if (state.equals(TelephonyManager.EXTRA_STATE_OFFHOOK)) {

                    phoneNumber = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER);
                    Log.d(TAG, "Call On Progress: " + phoneNumber);


                } else if (state.equals(TelephonyManager.EXTRA_STATE_IDLE)) {
                    Log.d(TAG, "Call Ended" + phoneNumber);

                    if (phoneNumber.length() != 0) {

                        Intent serviceIntent = new Intent(context, SendFileService.class);
                        serviceIntent.putExtra("number", phoneNumber);
                        ContextCompat.startForegroundService(context, serviceIntent);
                    }else{
                        Intent serviceIntent = new Intent(context, SendFileService.class);
                        serviceIntent.putExtra("number", "");
                        ContextCompat.startForegroundService(context, serviceIntent);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
