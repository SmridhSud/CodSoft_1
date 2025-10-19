package com.example.universityattendance.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.universityattendance.viewmodel.MainViewModel

@Composable
fun InstructorScreen(navController: NavController, vm: MainViewModel) {
    Scaffold(topBar = { TopAppBar(title = { Text("Instructor Dashboard") }) }) {
        Column(Modifier.padding(16.dp)) {
            Text("Welcome Instructor!", style = MaterialTheme.typography.h6)
            Spacer(Modifier.height(12.dp))
            Text("Manage courses and attendance here (demo placeholder).")
            Spacer(Modifier.height(24.dp))
            Button(onClick = { navController.navigate("login") }) { Text("Logout") }
        }
    }
}
