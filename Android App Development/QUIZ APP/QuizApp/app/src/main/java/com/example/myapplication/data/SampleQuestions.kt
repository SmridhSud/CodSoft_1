package com.example.quizapp.data

import com.example.quizapp.models.Question

val sampleQuestions = listOf(
    Question(
        id = 1,
        text = "What is the capital of France?",
        options = listOf("Berlin", "Madrid", "Paris", "Rome"),
        correctIndex = 2
    ),
    Question(
        id = 2,
        text = "Which language runs on the Android platform?",
        options = listOf("Swift", "Kotlin", "Ruby", "Go"),
        correctIndex = 1
    ),
    Question(
        id = 3,
        text = "Which planet is known as the Red Planet?",
        options = listOf("Earth", "Mars", "Jupiter", "Venus"),
        correctIndex = 1
    ),
    Question(
        id = 4,
        text = "Who wrote 'Romeo and Juliet'?",
        options = listOf("Charles Dickens", "William Shakespeare", "Mark Twain", "J.K. Rowling"),
        correctIndex = 1
    ),
    Question(
        id = 5,
        text = "What does HTML stand for?",
        options = listOf("HyperText Markup Language", "HighText Machine Language", "Hyperlink Text Markup Language", "None of the above"),
        correctIndex = 0
    )
)
