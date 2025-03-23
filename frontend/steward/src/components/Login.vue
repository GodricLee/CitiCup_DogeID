<template>
    <div class="login-container">
        <header class="app-header">
            <div class="logo-container">
                <img src="@/assets/logo.png" alt="DogeID Logo" class="logo" />
                <h1 class="app-title">DogeID: Steward</h1>
            </div>
            
        </header>

        <main class="main-content">
            <section class="hero-section">
                <h2 class="hero-title">Login With Your Wallet</h2>
            </section>

            <section class="login-section">
                <form @submit.prevent="handleSubmit">
                    <div class="form-group">
                        <label for="walletname" style="font-size: 1.5em;">Wallet Name</label>
                        <input
                            type="text"
                            id="walletname"
                            v-model="walletname"
                            placeholder="Enter your wallet name"
                            required
                        />
                    </div>
                    <div class="form-group">
                        <label for="password" style="font-size: 1.5em;">Wallet Key</label>
                        <input
                            type="password"
                            id="password"
                            v-model="password"
                            placeholder="Enter your wallet key"
                            required
                        />
                    </div>
                    <button type="submit">Open Wallet</button>
                </form>
                <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            </section>
        </main>

        <footer class="app-footer">
            <p>&copy; 2025 DogeID for Citi Cup. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
import api from '../api';

export default {
    data() {
        return {
            walletname: '',
            password: '',
            errorMessage: '',
        };
    },
    methods: {
        async handleSubmit() {
            try {
                const response = await api.post('/api/open_wallet', {
                    wallet_name: this.walletname,
                    wallet_key: this.password,
                });
                if (response.status !== 200) {
                    this.errorMessage = 'Login failed. Please check your wallet name and key.';
                    return;
                }
                localStorage.setItem('walletname', this.walletname);
                this.$router.push('/home');
            } catch (error) {
                this.errorMessage = 'Login failed. Please check your wallet name and key.';
                console.error('Login error:', error);
            }
        },
    },
};
</script>

<style scoped>
.login-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Reuse from Home */
.app-header {
    background: #333;
    color: #fff;
    padding: 1rem 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.logo-container {
    display: flex;
    align-items: center;
}

.logo {
    width: 60px;
    height: 60px;
    margin-right: 15px;
}

.app-title {
    margin: 0;
    font-size: 2em;
    font-weight: 500;
}

.main-nav {
    display: flex;
}

.nav-link {
    color: #fff;
    text-decoration: none;
    padding: 0.75rem 1rem;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}
.nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
    flex: 1;
    padding: 20px;
    margin: 1 auto;
    margin-top: 100px;
}

.hero-section {
    text-align: center;
    padding: 20px 0;
    background: #e9ecef;
    border-radius: 10px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 1.8em;
    color: #333;
    margin: 0;
}

.login-section {
    max-width: 400px;
    margin: 0 auto;
    background: #fff;
    padding: 20px;
    border-radius: 8px;
}

.form-group {
    margin-bottom: 15px;
}

input {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #4caf50;
    color: #fff;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

.error-message {
    color: red;
    margin-top: 10px;
}

.app-footer {
    text-align: center;
    padding: 1rem;
    background: #333;
    color: #fff;
}
</style>