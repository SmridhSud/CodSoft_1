package com.example.universityattendance.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.universityattendance.data.AppRepository
import com.example.universityattendance.models.User
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel(private val repo: AppRepository) : ViewModel() {

    private val _currentUser = MutableStateFlow<User?>(null)
    val currentUser: StateFlow<User?> get() = _currentUser

    fun register(username: String, password: String, role: String) {
        viewModelScope.launch { repo.register(User(username = username, password = password, role = role)) }
    }

    fun login(username: String, password: String, onSuccess: (User?) -> Unit) {
        viewModelScope.launch { onSuccess(repo.login(username, password)) }
    }

    fun logout() { _currentUser.value = null }

    companion object {
        fun provideFactory(repo: AppRepository): ViewModelProvider.Factory =
            object : ViewModelProvider.Factory {
                override fun <T : ViewModel> create(modelClass: Class<T>): T {
                    return MainViewModel(repo) as T
                }
            }
    }
}
