package com.example.universityattendance.ui

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.universityattendance.viewmodel.MainViewModel

@Composable
fun AppNavHost(navController: NavHostController, vm: MainViewModel) {
    NavHost(navController, startDestination = "login") {
        composable("login") { LoginScreen(navController, vm) }
        composable("student") { StudentScreen(navController, vm) }
        composable("instructor") { InstructorScreen(navController, vm) }
    }
}
