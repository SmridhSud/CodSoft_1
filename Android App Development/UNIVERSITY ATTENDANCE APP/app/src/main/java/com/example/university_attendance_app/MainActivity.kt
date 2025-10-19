package com.example.universityattendance

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.rememberNavController
import com.example.universityattendance.data.AppDatabase
import com.example.universityattendance.data.AppRepository
import com.example.universityattendance.ui.AppNavHost
import com.example.universityattendance.ui.theme.UniversityTheme
import com.example.universityattendance.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val db = AppDatabase.getInstance(this)
        val repo = AppRepository(db)
        setContent {
            UniversityTheme {
                val navController = rememberNavController()
                val mainVm: MainViewModel =
                    viewModel(factory = MainViewModel.provideFactory(repo))
                AppNavHost(navController, mainVm)
            }
        }
    }
}
