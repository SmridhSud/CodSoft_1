package com.example.universityattendance.data

import androidx.room.*
import com.example.universityattendance.models.User

@Dao
interface AppDao {
    @Insert suspend fun insertUser(user: User)
    @Query("SELECT * FROM users WHERE username=:username LIMIT 1")
    suspend fun getUser(username: String): User?
}
