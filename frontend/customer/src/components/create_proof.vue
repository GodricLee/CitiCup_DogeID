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
                <h2 class="hero-title">Create Proof</h2>
                <p class="hero-subtitle">Enter the required details to create a proof.</p>
            </section>

            <section class="features-section">
                <div class="feature-card">
                    <label>Proof Request:</label>
                    <textarea v-model="proofReq" rows="8" placeholder="Paste proof request here..."></textarea>
                </div>
                <div class="feature-card">
                    <label>Ready for Proof:</label>
                    <textarea v-model="readyForProof" rows="8" placeholder="Paste ready for proof here..."></textarea>
                </div>
                <div class="feature-card">
                    <label>Schema:</label>
                    <textarea v-model="schema" rows="8" placeholder="Paste schema here..."></textarea>
                </div>
                <div class="feature-card">
                    <label>Credential Definition:</label>
                    <textarea v-model="credDef" rows="8" placeholder="Paste credential definition here..."></textarea>
                </div>
            </section>
            <button @click="createProof" class="submit-button">Create Proof</button>

            <section class="features-section" v-if="proofList.length" style="text-align: center; display: flex; justify-content: center;">
                <div class="feature-card" style="text-align: center;">
                    <h2>Existing Proofs</h2>
                    <ul>
                        <li v-for="(proof, index) in proofList" :key="index" style="word-wrap: break-word;">
                            {{ proof }}
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
    name: "CreateProof",
    data() {
        return {
            proofReq: "",
            readyForProof: "",
            schema: "",
            credDef: "",
            proofList: [],
        };
    },
    created() {
        this.fetchProofs();
    },
    methods: {
        async createProof() {
            if (!this.proofReq || !this.readyForProof || !this.schema || !this.credDef) {
                alert("Fill all fields");
                return;
            }
            try {
                let jsonproofReq = this.proofReq;
                let jsonreadyForProof = this.readyForProof;
                let jsonschema = this.schema;
                let jsoncredDef = this.credDef;
                const res = await api.post("/api/create_proof", {
                    proof_req: jsonproofReq,
                    readyforproof: jsonreadyForProof,
                    schema: jsonschema,
                    cred_def: jsoncredDef,
                });
                alert("Proof created successfully");
                this.fetchProofs();
            } catch (error) {
                console.error(error);
            }
        },
        async fetchProofs() {
            try {
                const res = await api.post("/api/list_proof");
                if (res.data.status === "success") {
                    this.proofList = res.data.message || [];
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