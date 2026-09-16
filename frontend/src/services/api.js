const API_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function parseResponse(response, defaultMessage) {
  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error(defaultMessage);
  }

  if (!response.ok) {
    throw new Error(data.detail || defaultMessage);
  }

  return data;
}

export async function researchCompany(companyName) {
  const response = await fetch(`${API_URL}/api/v1/research`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      company_name: companyName,
    }),
  });

  const data = await parseResponse(
    response,
    "Unable to research the company."
  );

  return data.result;
}

export async function uploadDocument(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_URL}/api/v1/ingest`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(
    response,
    "Unable to upload the document."
  );
}

export async function askQuestion(question) {
  const response = await fetch(`${API_URL}/api/v1/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  const data = await parseResponse(
    response,
    "Unable to answer the question."
  );

  return data.result;
}