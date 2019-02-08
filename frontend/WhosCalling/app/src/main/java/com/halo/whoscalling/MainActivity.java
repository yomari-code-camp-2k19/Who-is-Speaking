package com.halo.whoscalling;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    EditText et_ip;
    Button btn_setIp;

    SharedPreferences sharedPreferences;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        et_ip = findViewById(R.id.et_ip);
        btn_setIp = findViewById(R.id.btn_setIp);

        btn_setIp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                SharedPreferences.Editor editor = getSharedPreferences("ip_address", MODE_PRIVATE).edit();
                editor.putString("ip", et_ip.getText().toString().trim());
                editor.apply();
            }
        });
    }
}
