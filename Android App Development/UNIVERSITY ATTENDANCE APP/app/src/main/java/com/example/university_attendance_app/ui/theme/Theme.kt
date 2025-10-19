package com.example.universityattendance.ui.theme

import androidx.compose.material.MaterialTheme
import androidx.compose.material.lightColors
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColors(
    primary = Color(0xFF1976D2),
    secondary = Color(0xFF03DAC5)
)

@Composable
fun UniversityTheme(content: @Composable () -> Unit) {
    MaterialTheme(colors = LightColors, content = content)
}
