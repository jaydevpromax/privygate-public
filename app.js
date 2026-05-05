const scenarios = {
  alice: {
    name: "Alice request",
    accepted: true,
    reason: "policy satisfied",
    matched: "University:role:student, Lab:role:researcher",
    storageDecision: "Alice accepted policy-bound tool access",
    hashSeed: "alice|ResearchAgent|private-dataset.read|student|researcher|epoch1",
    events: [
      "registerAuthority(University)",
      "registerAuthority(Lab)",
      "registerPolicy(ResearchPolicy)",
      "recordVerification(success)"
    ]
  },
  bob: {
    name: "Bob request",
    accepted: false,
    reason: "insufficient non-revoked credentials for policy",
    matched: "University:role:student",
    storageDecision: "Bob rejected before protected tool access",
    hashSeed: "bob|ResearchAgent|private-dataset.read|student-only|epoch1",
    events: [
      "registerAuthority(University)",
      "registerAuthority(Lab)",
      "registerPolicy(ResearchPolicy)",
      "recordVerification(rejected)"
    ]
  },
  revoked: {
    name: "Alice after revocation",
    accepted: false,
    reason: "credential revoked: Lab:role:researcher",
    matched: "University:role:student",
    storageDecision: "Revoked credential blocks old Alice authorization",
    hashSeed: "alice|ResearchAgent|private-dataset.read|revoked-researcher|epoch1",
    events: [
      "registerAuthority(University)",
      "registerAuthority(Lab)",
      "registerPolicy(ResearchPolicy)",
      "setRevoked(Alice researcher credential)",
      "recordVerification(after revocation)"
    ]
  }
};

const resultBadge = document.getElementById("resultBadge");
const scenarioName = document.getElementById("scenarioName");
const resultReason = document.getElementById("resultReason");
const matchedAttributes = document.getElementById("matchedAttributes");
const auditHash = document.getElementById("auditHash");
const storageDecision = document.getElementById("storageDecision");
const registryEvents = document.getElementById("registryEvents");
const actorButtons = Array.from(document.querySelectorAll("[data-scenario]"));

function stableHash(input) {
  let value = 0x811c9dc5;
  for (let i = 0; i < input.length; i += 1) {
    value ^= input.charCodeAt(i);
    value = Math.imul(value, 0x01000193);
  }
  return (value >>> 0).toString(16).padStart(8, "0");
}

function renderScenario(key) {
  const scenario = scenarios[key];
  scenarioName.textContent = scenario.name;
  resultReason.textContent = scenario.reason;
  matchedAttributes.textContent = scenario.matched;
  storageDecision.textContent = scenario.storageDecision;
  auditHash.textContent = `audit:${stableHash(scenario.hashSeed)}${stableHash(scenario.reason)}`;

  resultBadge.classList.toggle("accept", scenario.accepted);
  resultBadge.classList.toggle("reject", !scenario.accepted);
  resultBadge.querySelector(".result-label").textContent = scenario.accepted ? "ACCEPT" : "REJECT";

  registryEvents.replaceChildren(
    ...scenario.events.map((eventName) => {
      const item = document.createElement("li");
      item.textContent = eventName;
      return item;
    })
  );

  actorButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.scenario === key);
  });
}

actorButtons.forEach((button) => {
  button.addEventListener("click", () => {
    renderScenario(button.dataset.scenario);
  });
});

renderScenario("alice");
