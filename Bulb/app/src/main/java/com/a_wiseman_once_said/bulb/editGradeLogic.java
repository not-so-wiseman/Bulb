package com.a_wiseman_once_said.bulb;

import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.content.Context;
import android.widget.EditText;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatDialogFragment;

import org.json.JSONException;

public class editGradeLogic extends AppCompatDialogFragment {
    private EditText editGoal;
    private EditGradeDialogListener listener;

    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());

        LayoutInflater inflater = getActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.edit_goal_dialog, null);

        builder.setView(view)
                .setTitle("Edit your goal for the course")
                .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {

                    }
                })
                .setPositiveButton("apply", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        String goal = editGoal.getText().toString();
                        try {
                            listener.applyTexts(goal);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                });

        editGoal = view.findViewById(R.id.editGoal);

        return builder.create();
    }


    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        try {
            listener = (EditGradeDialogListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context.toString() +
                    "must implement EditGradeDialogListener");
        }
    }

    public interface EditGradeDialogListener {
        void applyTexts(String goal) throws JSONException;
    }
}
