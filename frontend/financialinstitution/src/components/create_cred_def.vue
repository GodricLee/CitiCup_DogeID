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
                <h2 class="hero-title">Create Credential Definition</h2>
                <p class="hero-subtitle">Select DID and Schema, then create a new credential definition on the ledger.</p>
            </section>

            <section class="features-section">
                <div class="feature-card">
                    <label>Your DID:</label>
                    <select v-model="selectedMydid">
                        <option v-for="didItem in mydidList" :key="didItem.did" :value="didItem.did">
                            {{ didItem.did }}
                        </option>
                    </select>
                </div>
                <div class="feature-card">
                    <label>Schema:</label>
                    <select v-model="selectedSchema">
                        <option v-for="schema in schemaList" :key="schema" :value="schema">
                            {{ schema }}
                        </option>
                    </select>
                </div>
                <div class="feature-card">
                    <label>Tag:</label>
                    <input v-model="tag" type="text" placeholder="e.g. tag1" />
                </div>
                <div class="feature-card">
                    <label>Config (optional):</label>
                    <input v-model="config" type="text" placeholder='e.g. {"support_revocation": false}' />
                </div>
            </section>
            <button @click="createCredDef" class="submit-button">Submit Credential Definition</button>

            <section class="features-section" v-if="credDefList.length" style="text-align: center; display: flex; justify-content: center;">
                <div class="feature-card" style="text-align: center;">
                    <h2>Existing Credential Definitions</h2>
                    <ul>
                        <li v-for="(credDef, index) in credDefList" :key="index" style="word-wrap: break-word;">
                            {{ credDef }}
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
import api from '../api';

export default {
    name: "CreateCredDef",
    data() {
        return {
            mydidList: [],
            selectedMydid: "",
            schemaList: [],
            selectedSchema: "",
            tag: "",
            config: "",
            credDefList: [],
        };
    },
    created() {
        this.fetchMyDids();
        this.fetchSchemas();
        this.fetchCredDefs();
    },
    methods: {
        async fetchMyDids() {
            try {
                const res = await api.get("/api/list_did");
                if (res.data.status === "success") {
                    const dids = JSON.parse(res.data.message);
                    this.mydidList = dids.map((item) => ({
                        did: item.did,
                        verkey: item.verkey,
                    }));
                }
            } catch (error) {
                console.error(error);
            }
        },
        async fetchSchemas() {
            try {
                const res = await api.get("/api/list_schema");
                if (res.data.status === "success") {
                    this.schemaList = res.data.message || [];
                }
            } catch (error) {
                console.error(error);
            }
        },
        async createCredDef() {
            if (!this.selectedMydid || !this.selectedSchema || !this.tag) {
                alert("Fill all fields");
                return;
            }
            try {
                await api.post("/api/create_cred_def", {
                    mydid: this.selectedMydid,
                    schema: JSON.parse(this.selectedSchema),
                    tag: this.tag,
                    config: this.config ? JSON.parse(this.config) : null,
                });
                alert("Credential Definition created");
                this.fetchCredDefs();
            } catch (error) {
                console.error(error);
            }
        },
        async fetchCredDefs() {
            try {
                const res = await api.get("/api/list_cred_def");
                if (res.data.status === "success") {
                    this.credDefList = res.data.message || [];
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
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    justify-content: center;
    max-width: 600px;
}
.feature-card {
    background: #f8f8f8;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    justify-content: center;
    max-width: 600px;
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