<template>
    <div class="home-container">
        <header class="app-header">
            <div class="logo-container">
                <img src="@/assets/logo.png" alt="DogeID Logo" class="logo" />
                <h1 class="app-title">DogeID: Customer</h1>
            </div>
            <nav class="main-nav">
                <router-link to="/home" class="nav-link">Home</router-link>
                <router-link to="/create_did" class="nav-link">Create DID</router-link>
                <router-link to="/create_cred_req" class="nav-link">Create Credential Request</router-link>
                <router-link to="/store_credential" class="nav-link">Store Credential</router-link>
                <router-link to="/list_cred" class="nav-link">List Credentials</router-link>
                <router-link to="/create_proof" class="nav-link">Create Proof</router-link>
            </nav>
        </header>

        <main class="main-content">
            <section class="hero-section">
                <h2 class="hero-title">My DIDs</h2>
                <p class="hero-subtitle">Below is a list of all DIDs in the current wallet:</p>
                <ul v-if="mydidList.length">
                    <li v-for="item in mydidList" :key="item.did">
                        {{ item.did }} - {{ item.verkey }}
                    </li>
                </ul>
                <p v-else>No DIDs found.</p>
            </section>

            <section class="features-section">
                <div class="feature-card">
                    <label>Seed:</label>
                    <input v-model="seed" type="text" placeholder="Enter seed..." />
                </div>
            </section>
            <button @click="createDid" class="submit-button">Create DID</button>
        </main>

        <footer class="app-footer">
            <p>&copy; 2025 DogeID for Citi Cup. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
import api from '../api';

export default {
    name: "CreateDid",
    data() {
        return {
            mydidList: [],
            seed: "",
        };
    },
    created() {
        this.fetchMyDids();
    },
    methods: {
        async fetchMyDids() {
            try {
                const res = await api.get("/api/list_did");
                const { status, message } = res.data;
                if (status === "success") {
                    const dids = JSON.parse(message);
                    this.mydidList = dids.map((item) => ({
                        did: item.did,
                        verkey: item.verkey,
                    }));
                }
            } catch (error) {
                console.error(error);
            }
        },
        async createDid() {
            if (!this.seed) {
                alert("Please enter a seed");
                return;
            }
            try {
                await api.post("/api/create_did", { seed: this.seed });
                alert("DID created");
                this.seed = "";
                this.fetchMyDids();
            } catch (error) {
                console.error(error);
            }
        },
    },
};
</script>

<style scoped>
body {
    font-family: "Arial", sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f4f4f4;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.submit-button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.2em;
}

.home-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin-top: 0;
}
.main-content {
    flex: 1;
    padding: 20px;
    margin: 0 auto;
    margin-top: 100px;
}
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
    font-size: 1em;
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
.hero-section {
    text-align: center;
    padding: 50px 0;
    background: #e9ecef;
    border-radius: 10px;
    margin-bottom: 20px;
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
.features-section {
    padding: 30px 0;
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}
.feature-card {
    background: #f8f8f8;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.feature-card label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}
.feature-card input,
.feature-card select {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
}
.app-footer {
    text-align: center;
    padding: 1rem;
    background: #333;
    color: #fff;
}
</style>
