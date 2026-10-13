package com.example.saygo.imefixture;

import android.app.Activity;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

/** An offline screen for observing automated and human keyboard input. */
public final class InputActivity extends Activity {
    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        int padding = (int) (24 * getResources().getDisplayMetrics().density);
        content.setPadding(padding, padding * 2, padding, padding);

        TextView title = new TextView(this);
        title.setText("Input handoff test");
        title.setTextSize(26);
        content.addView(title);

        TextView instructions = new TextView(this);
        instructions.setText("Offline fixture. Use sample text only.\n"
            + "Both fields accept Chinese and English.\n"
            + "Human checks require a person to type on the keyboard.");
        instructions.setTextSize(16);
        content.addView(instructions);

        addField(content, 1, "Automatic input", "Tap here for automated input");
        addField(content, 2, "Human input", "Tap here and type yourself");

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.addView(content);
        setContentView(scroll);
        content.setFocusableInTouchMode(true);
        content.requestFocus();
    }

    private void addField(LinearLayout content, int id, String label, String hint) {
        TextView heading = new TextView(this);
        heading.setText("\n" + label);
        heading.setTextSize(20);
        content.addView(heading);

        EditText field = new EditText(this);
        field.setId(id);
        field.setHint(hint);
        field.setTextSize(22);
        field.setMinLines(2);
        field.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        if (android.os.Build.VERSION.SDK_INT >= 26) {
            field.setImportantForAutofill(View.IMPORTANT_FOR_AUTOFILL_NO);
        }
        content.addView(field, new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
    }
}
