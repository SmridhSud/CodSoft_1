package com.example.quizapp.viewmodel

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.quizapp.data.sampleQuestions
import com.example.quizapp.models.Question
import kotlin.random.Random

class QuizViewModel : ViewModel() {

    var questions: List<Question> by mutableStateOf(sampleQuestions)
        private set

    var currentIndex by mutableStateOf(0)
        private set

    var selectedOptionIndex by mutableStateOf<Int?>(null)
        private set

    var score by mutableStateOf(0)
        private set

    var showAnswerFeedback by mutableStateOf(false)
        private set

    fun startQuiz(randomize: Boolean = false) {
        questions = if (randomize) questions.shuffled(Random(System.currentTimeMillis())) else sampleQuestions
        currentIndex = 0
        selectedOptionIndex = null
        score = 0
        showAnswerFeedback = false
    }

    fun selectOption(index: Int) {
        if (showAnswerFeedback) return // prevent changing after reveal
        selectedOptionIndex = index
    }

    fun submitAnswer() {
        val q = questions[currentIndex]
        val selected = selectedOptionIndex
        if (selected != null) {
            if (selected == q.correctIndex) {
                score += 1
            }
        }
        showAnswerFeedback = true
    }

    fun nextQuestion(): Boolean {
        // returns true if there are more questions, false if finished
        if (currentIndex < questions.lastIndex) {
            currentIndex++
            selectedOptionIndex = null
            showAnswerFeedback = false
            return true
        }
        return false
    }

    fun restart(randomize: Boolean = false) {
        startQuiz(randomize)
    }
}
