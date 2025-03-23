<template>
    <div class="home-container">
        <header class="app-header">
            <div class="logo-container">
                <img src="@/assets/logo.png" alt="DogeID Logo" class="logo" />
                <h1 class="app-title">DogeID: Steward</h1>
            </div>
            <nav class="main-nav">
                <router-link to="/home" class="nav-link">Home</router-link>
                <router-link to="/create_user" class="nav-link">Create User</router-link>
            </nav>
        </header>

        <main class="main-content">
            <section class="hero-section">
                <h2 class="hero-title">Welcome to DogeID: Steward</h2>
                <p class="hero-subtitle">Your decentralized identity management system.</p>
            </section>

            <section class="features-section">
                <h3>Key Features</h3>
                <div class="features-grid">
                    <div class="feature-card">
                        <h4>Create Wallet</h4>
                        <p>Initialize a new wallet for storing your DIDs and credentials securely.</p>
                    </div>
                    <div class="feature-card">
                        <h4>Open Wallet</h4>
                        <p>Access your existing wallet using your wallet name and key.</p>
                    </div>
                    <div class="feature-card">
                        <h4>Create DID</h4>
                        <p>Generate a new Decentralized Identifier (DID) within your wallet.</p>
                    </div>
                    <div class="feature-card">
                        <h4>List DIDs</h4>
                        <p>View all the DIDs stored in your wallet for easy management.</p>
                    </div>
                    <div class="feature-card">
                        <h4>Create User</h4>
                        <p>Register new users by creating DIDs and assigning specific roles.</p>
                    </div>
                </div>
            </section>

            <section class="cta-section">
                <p>Ready to get started? Explore the functionalities using the navigation above.</p>
            </section>
        </main>

        <footer class="app-footer">
            <p>&copy; 2025 DogeID for Citi Cup. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
export default {
    name: "Home",
};
</script>

<style scoped>
/* General Styles */
body {
    font-family: "Arial", sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f4f4f4;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

/* Layout */
.home-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin-top: 0;
}

.main-content {
    flex: 1;
    padding: 20px;
    margin: 1 auto;
    margin-top: 100px; /* Adjust this value to avoid content being hidden behind the fixed header */
}

/* Header Styles */
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

/* Navigation Styles */
.main-nav {
    display: flex;
    font-size: 1.3em; /* Increase the font size */
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

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 50px 0;
    background: #e9ecef;
    border-radius: 10px;
}

.hero-title {
    font-size: 2.5em;
    color: #333;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 1.2em;
    color: #555;
}

/* Features Section */
.features-section {
    padding: 30px 0;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.feature-card {
    background: #f8f8f8;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature-card h4 {
    color: #007bff;
    margin-bottom: 10px;
}

/* CTA Section */
.cta-section {
    text-align: center;
    padding: 40px 0;
    background: #efefefe0;
    border-radius: 10px;
}

/* Footer Styles */
.app-footer {
    text-align: center;
    padding: 1rem;
    background: #333;
    color: #fff;
}
</style>
