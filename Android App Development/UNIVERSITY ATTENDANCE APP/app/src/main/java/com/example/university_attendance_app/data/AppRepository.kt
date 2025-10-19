package com.example.universityattendance.data

import com.example.universityattendance.models.User

class AppRepository(private val db: AppDatabase) {
    private val dao = db.dao()

    suspend fun register(user: User) = dao.insertUser(user)
    suspend fun login(username: String, password: String): User? {
        val user = dao.getUser(username)
        return if (user?.password == password) user else null
    }
}
