<template>
    <div class="home-container">
        <header class="app-header">
            <div class="logo-container">
                <img src="@/assets/logo.png" alt="DogeID Logo" class="logo" />
                <h1 class="app-title">DogeID: Financial Institution</h1>
            </div>
            <nav class="main-nav">
                <router-link to="/home" class="nav-link">Home</router-link>
                <router-link to="/create_did" class="nav-link">Create DID</router-link>
                <router-link to="/create_user" class="nav-link">Create User</router-link>
                <router-link to="/create_schema" class="nav-link">Create Schema</router-link>
                <router-link to="/create_cred_def" class="nav-link">Create Credential Definition</router-link>
                <router-link to="/create_cred_offer" class="nav-link">Create Credential Offer</router-link>
                <router-link to="/create_cred" class="nav-link">Create Credential</router-link>
                <router-link to="/verify_proof" class="nav-link">Verify Proof</router-link>
            </nav>
        </header>

        <main class="main-content">
            <section class="hero-section">
                <h2 class="hero-title">Create Credential</h2>
                <p class="hero-subtitle">Select Credential Offer and provide Credential Request and Credential Values below.</p>
            </section>

            <section class="features-section">
                <div class="feature-card">
                    <label>Credential Offer:</label>
                    <select v-model="selectedCredOffer">
                        <option v-for="(offer, index) in credOfferList" :key="index" :value="offer">
                            {{ offer }}
                        </option>
                    </select>
                </div>
                <div class="feature-card">
                    <label>Credential Request:</label>
                    <textarea v-model="credRequest" rows="8" placeholder="Paste credential request here..."></textarea>
                </div>
                <div class="feature-card">
                    <label>Credential Values:</label>
                    <textarea v-model="credValues" rows="8" placeholder="Paste credential values here..."></textarea>
                </div>
            </section>
            <button @click="createCredential" class="submit-button">Submit Credential</button>

            <section class="features-section" v-if="credList.length" style="text-align: center; display: flex; justify-content: center;">
                <div class="feature-card" style="text-align: center;">
                    <h2>Existing Credentials</h2>
                    <ul>
                        <li v-for="(cred, index) in credList" :key="index" style="word-wrap: break-word;">
                            {{ cred }}
                        </li>
                    </ul>
                </div>
            </section>
        </main>

        <footer class="app-footer">
            <p>&copy; 2025 DogeID for Citi Cup. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
import api from "../api";

export default {
    name: "CreateCred",
    data() {
        return {
            credOfferList: [],
            selectedCredOffer: "",
            credRequest: "",
            credValues: "",
            credList: [],
        };
    },
    created() {
        this.fetchCredOffers();
        this.fetchCreds();
    },
    methods: {
        async fetchCredOffers() {
            try {
                const res = await api.get("/api/list_cred_offer");
                const { status, message } = res.data;
                if (status === "success") {
                    this.credOfferList = message || [];
                }
            } catch (error) {
                console.error(error);
            }
        },

        async createCredential() {
            if (!this.selectedCredOffer || !this.credRequest || !this.credValues) {
                alert("Fill all fields");
                return;
            }
            try {
                await api.post("/api/create_credential", {
                    cred_offer: JSON.parse(this.selectedCredOffer),
                    cred_request: JSON.parse(this.credRequest),
                    cred_values: JSON.parse(this.credValues),
                });
                alert("Credential created");
                this.credRequest = "";
                this.credValues = "";
                this.fetchCreds();
            } catch (error) {
                console.error(error);
            }
        },

        async fetchCreds() {
            try {
                const res = await api.get("/api/list_cred");
                const { status, message } = res.data;
                if (status === "success") {
                    this.credList = message || [];
                }
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
    max-width: 600px;
}
.feature-card {
    background: #f8f8f8;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 600px;
}
.feature-card label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}
.feature-card input,
.feature-card select,
.feature-card textarea {
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