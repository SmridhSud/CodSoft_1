package com.example.quizapp.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.example.quizapp.viewmodel.QuizViewModel

@Composable
fun HomeScreen(navController: NavController, vm: QuizViewModel = viewModel()) {
    Surface(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Quiz App", fontSize = 32.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = {
                vm.startQuiz(randomize = false)
                navController.navigate("quiz")
            }, modifier = Modifier.fillMaxWidth()) {
                Text("Start Quiz")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Button(onClick = {
                vm.startQuiz(randomize = true)
                navController.navigate("quiz")
            }, modifier = Modifier.fillMaxWidth()) {
                Text("Start Random Quiz")
            }
            Spacer(modifier = Modifier.height(20.dp))
            Text("Questions: ${vm.questions.size}", color = Color.Gray)
        }
    }
}

@Composable
fun QuizScreen(navController: NavController, vm: QuizViewModel = viewModel()) {
    val q = vm.questions[vm.currentIndex]

    Column(modifier = Modifier
        .fillMaxSize()
        .padding(16.dp)) {
        Text(text = "Question ${vm.currentIndex + 1} / ${vm.questions.size}", fontWeight = FontWeight.SemiBold)
        Spacer(modifier = Modifier.height(8.dp))
        Card(
            elevation = 4.dp,
            shape = RoundedCornerShape(8.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(q.text, fontSize = 20.sp)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Column(modifier = Modifier.fillMaxWidth()) {
            q.options.forEachIndexed { idx, option ->
                val isSelected = vm.selectedOptionIndex == idx
                val isCorrect = vm.showAnswerFeedback && idx == q.correctIndex
                val isIncorrectSelected = vm.showAnswerFeedback && isSelected && !isCorrect

                val bg = when {
                    isCorrect -> Color(0xFFa5d6a7) // green
                    isIncorrectSelected -> Color(0xFFef9a9a) // red
                    isSelected -> Color(0xFFBBDEFB) // light blue
                    else -> Color.White
                }

                Card(modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 6.dp)
                    .clickable(enabled = !vm.showAnswerFeedback) { vm.selectOption(idx) },
                    elevation = 2.dp) {
                    Row(modifier = Modifier
                        .background(bg)
                        .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically) {
                        Text(text = option, fontSize = 16.sp)
                    }
                }
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Score: ${vm.score}", fontWeight = FontWeight.Bold)
            Row {
                if (!vm.showAnswerFeedback) {
                    Button(onClick = { vm.submitAnswer() }, enabled = vm.selectedOptionIndex != null) {
                        Text("Submit")
                    }
                } else {
                    Button(onClick = {
                        val hasMore = vm.nextQuestion()
                        if (!hasMore) {
                            navController.navigate("result")
                        }
                    }) {
                        Text(if (vm.currentIndex < vm.questions.lastIndex) "Next" else "See Result")
                    }
                }
            }
        }
    }
}

@Composable
fun ResultScreen(navController: NavController, vm: QuizViewModel = viewModel()) {
    Surface(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
            Text("Quiz Result", fontSize = 28.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(12.dp))
            Text("Score: ${vm.score} / ${vm.questions.size}", fontSize = 22.sp)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = {
                vm.restart(randomize = false)
                navController.navigate("quiz") {
                    popUpTo("home") // simple navigation cleanup
                }
            }, modifier = Modifier.fillMaxWidth()) {
                Text("Retry")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Button(onClick = {
                vm.restart(randomize = true)
                navController.navigate("quiz") {
                    popUpTo("home")
                }
            }, modifier = Modifier.fillMaxWidth()) {
                Text("Retry (Random)")
            }
            Spacer(modifier = Modifier.height(12.dp))
            OutlinedButton(onClick = {
                navController.navigate("home") {
                    popUpTo("home")
                }
            }, modifier = Modifier.fillMaxWidth()) {
                Text("Back to Home")
            }
        }
    }
}
