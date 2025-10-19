plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'kotlin-kapt'
}

android {
    namespace 'com.example.universityattendance'
    compileSdk 31

    defaultConfig {
        applicationId "com.example.universityattendance"
        minSdk 21
        targetSdk 31
        versionCode 1
        versionName "1.0"
    }

    buildFeatures {
        compose true
    }

    composeOptions {
        kotlinCompilerExtensionVersion '1.5.3'
    }

    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    implementation "androidx.core:core-ktx:1.11.0"
    implementation "androidx.activity:activity-compose:1.8.0"
    implementation "androidx.lifecycle:lifecycle-viewmodel-compose:2.6.1"
    implementation "androidx.lifecycle:lifecycle-runtime-ktx:2.6.1"
    implementation "androidx.navigation:navigation-compose:2.7.0"

    // Jetpack Compose
    implementation "androidx.compose.ui:ui:1.5.0"
    implementation "androidx.compose.material:material:1.5.0"
    implementation "androidx.compose.ui:ui-tooling-preview:1.5.0"
    debugImplementation "androidx.compose.ui:ui-tooling:1.5.0"

    // Room database
    implementation "androidx.room:room-runtime:2.5.2"
    kapt "androidx.room:room-compiler:2.5.2"
    implementation "androidx.room:room-ktx:2.5.2"
}
