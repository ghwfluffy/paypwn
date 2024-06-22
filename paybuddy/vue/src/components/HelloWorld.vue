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
import { StatusRequest, StatusResponse } from "@/proto/api/Status";

defineProps<{ msg: string }>();

const serverStatus = ref("Uninitialized");

async function getStatus() {
  // Create request
  const request = StatusRequest.create({});
  request.context = "Hello World.";

  // Serialize the request to a binary format
  const requestData = StatusRequest.toJSON(request);

  // Convert JSON object to URL query string
  const queryParams = new URLSearchParams(requestData as string[][]).toString();

  try {
    // Send the GET request to the server with query parameters
    const response = await fetch(`api/status?${queryParams}`, {
      method: 'GET',
    });

    // Read the response as an ArrayBuffer
    const responseData = await response.json();

    // Parse the response
    const statusResponse = StatusResponse.fromJSON(responseData);

    // Update the serverStatus
    serverStatus.value = "Server version: " + statusResponse.version;
  } catch (error) {
    serverStatus.value = "Error fetching status: " + String(error);
  }
}
</script>
