
-- Tabla para almacenar los usuarios
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para almacenar las listas de tareas
CREATE TABLE lists (
    list_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    list_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Tabla para almacenar las tareas
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    list_id INT NOT NULL,
    task_name VARCHAR(100) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (list_id) REFERENCES lists(list_id) ON DELETE CASCADE
);

-- Tabla para almacenar las API keys (protección del backend)
CREATE TABLE api_keys (
    api_key_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    api_key VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_lists_user_id ON lists(user_id);
CREATE INDEX idx_tasks_list_id ON tasks(list_id);
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);