package com.example.universityattendance.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.universityattendance.viewmodel.MainViewModel

@Composable
fun LoginScreen(navController: NavController, vm: MainViewModel) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var role by remember { mutableStateOf("student") }
    var isRegister by remember { mutableStateOf(false) }
    val scaffoldState = rememberScaffoldState()

    Scaffold(scaffoldState = scaffoldState) {
        Column(Modifier.padding(16.dp)) {
            Text(if (isRegister) "Register" else "Login", style = MaterialTheme.typography.h5)
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(username, { username = it }, label = { Text("Username") }, Modifier.fillMaxWidth())
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(password, { password = it }, label = { Text("Password") },
                visualTransformation = PasswordVisualTransformation(), modifier = Modifier.fillMaxWidth())
            Spacer(Modifier.height(8.dp))
            Row {
                RadioButton(selected = role == "student", onClick = { role = "student" })
                Text("Student", Modifier.padding(end = 8.dp))
                RadioButton(selected = role == "instructor", onClick = { role = "instructor" })
                Text("Instructor")
            }
            Spacer(Modifier.height(16.dp))
            Button(onClick = {
                if (isRegister) {
                    vm.register(username, password, role)
                    isRegister = false
                    scaffoldState.snackbarHostState.showSnackbar("Registered successfully! Please log in.")
                } else {
                    vm.login(username, password) { user ->
                        if (user != null) {
                            if (user.role == "student") navController.navigate("student")
                            else navController.navigate("instructor")
                        } else {
                            scaffoldState.snackbarHostState.showSnackbar("Invalid credentials")
                        }
                    }
                }
            }, modifier = Modifier.fillMaxWidth()) {
                Text(if (isRegister) "Register" else "Login")
            }
            TextButton(onClick = { isRegister = !isRegister }) {
                Text(if (isRegister) "Already have an account? Login" else "No account? Register")
            }
        }
    }
}
