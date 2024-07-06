<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <button type="button" @click="getStatus()">
      {{ serverStatus }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { StatusRequest, StatusResponse } from "@/proto/api/Status";

defineProps<{ msg: string }>();

const serverStatus = ref("Uninitialized");

async function getStatus() {
  // Create request
  const request = StatusRequest.create({});
  request.context = "Hello World.";

  // Serialize the request to a JSON format
  const requestData = StatusRequest.toJSON(request);

  try {
    // Send the GET request to the server with query parameters
    const response = await axios.get("/api/status", {
      params: requestData,
    });

    // Parse the response
    const statusResponse = StatusResponse.fromJSON(response.data);

    // Update the serverStatus
    serverStatus.value = "Server version: " + statusResponse.version;
  } catch (error) {
    // Handle Axios errors
    if (axios.isAxiosError(error)) {
      serverStatus.value =
        "Error fetching status: " +
        (error.response ? error.response.data : error.message);
      // Other error
    } else {
      serverStatus.value = "Error fetching status: " + String(error);
    }
  }
}
</script>
