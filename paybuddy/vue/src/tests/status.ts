import axios from "axios";
import { StatusRequest, StatusResponse } from "@/proto/api/Status";

const API_BASE_URL = process.env.API_BASE_URL;

describe("API Tests", () => {
  it("should fetch the status", async () => {
    const contextString = "Hello World.";
    // Create a StatusRequest object
    const request = StatusRequest.create({ context: contextString });

    // Serialize the request to JSON
    const requestData = StatusRequest.toJSON(request);

    // Send the GET request to the server with query parameters
    const response = await axios.get(`${API_BASE_URL}/status`, {
      params: requestData,
    });

    // Parse the response
    const statusResponse = StatusResponse.fromJSON(response.data);

    // Validate the response
    expect(statusResponse.version).toBeDefined();
    expect(statusResponse.version).toBe("0.1");

    expect(statusResponse.context).toBeDefined();
    expect(statusResponse.context).toBe(contextString);
  });
});
