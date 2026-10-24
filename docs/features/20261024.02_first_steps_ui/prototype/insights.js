// The first readout's insights, written by hand for the prototype from the evidence in data.js.
// Each ref is a piece of a claim's text; app.js turns it into that claim's evidence number.
// In the built app, the readout writes these from the claims (Benjamin's research).
window.TC_INSIGHTS = {
  ploy: [
    { mark: "strong", piece: "The round", title: "The seed round is real and fully raised.",
      text: "Press reports a $27M seed led by First Round Capital and Y Combinator. The SEC filing agrees: every dollar offered was sold, to 11 investors, and $11,572,000 of it came from SAFEs that converted.",
      refs: ["Press reports a $27M seed", "$26,571,989 sold", "came from SAFEs that converted", "11 investors", "Form D filed"] },
    { mark: "strong", piece: "Team", title: "The founder has built this kind of company before.",
      text: "Bryant Chou was co-founder and CTO of Webflow for 12 years, and of Vungle before that. Webflow is one of the tools Ploy says it moves sites away from.",
      refs: ["Co-founder and CTO of Webflow", "co-founder and CTO of Vungle", "Signed the Form D as Chief Executive Officer", "moves sites over from"] },
    { mark: "mixed", piece: "Traction", title: "Early demand signals, but no revenue is public.",
      text: "Press names Hex and Clay as customers, and the company says over 13% of its batch use Ploy. Both come from the company's side. The SEC filing declines to disclose revenue, so this goes on the data-room request.",
      refs: ["Press names Hex and Clay", "over 13% of the batch", "Prices: Free $0"] },
    { mark: "weak", piece: "Market", title: "A crowded field with well-funded rivals.",
      text: "Ploy measures itself against Framer, Vercel, Lovable, Bolt and v0, and two companies in its own batch pitch nearly the same thing.",
      refs: ["comparison pages against Framer", "Sherpa", "Revnu"] },
    { mark: "strong", piece: "Outside world", title: "Developers pay attention, and nobody is complaining.",
      text: "A post on its engineering drew 258 points and 131 comments on Hacker News. No story or comment about Ploy uses dispute language.",
      refs: ["drew 258 points", "No Hacker News story or comment naming Ploy"] },
    { mark: "thin", piece: "Burn and runway", title: "Spending is unknown until the room arrives.",
      text: "The team is 14 people with one open role. Nothing public shows burn or runway after the seed.",
      refs: ["Team size on YC: 14", "Hiring: one open role"] },
  ],
  sazabi: [
    { mark: "mixed", piece: "The round", title: "The round is announced but not filed.",
      text: "The company says it raised an $8M seed co-led by J2 Ventures, Village Global and Y Combinator. EDGAR shows no Form D, and in April the company said it was still raising.",
      refs: ["$8M seed co-led", "returned 0 Form D filings", "still raising its seed"] },
    { mark: "strong", piece: "Team", title: "The founder knows this problem from the inside.",
      text: "A second-time YC founder who started the infrastructure and observability teams at Brex. Three of the nine engineers come from Brex, and he has a YC talk on the problem.",
      refs: ["second-time YC founder", "observability teams at Brex", "nine engineers", "The End of Manual Debugging"] },
    { mark: "mixed", piece: "Traction", title: "Strong early usage, all in the company's own words.",
      text: "It reports 50 design partners in under a month, 35 teams onboarded, 8,000 investigations and 2 TB of logs. None of it is confirmed outside the company yet.",
      refs: ["50 design partners", "onboarded 35 teams", "Case studies on its site"] },
    { mark: "weak", piece: "Outside world", title: "Little outside attention so far.",
      text: "Three Hacker News stories link to the site, and the largest has 2 points. Nobody disputes it, but few have noticed it.",
      refs: ["Little attention so far", "No Hacker News story or comment naming Sazabi"] },
    { mark: "mixed", piece: "Market", title: "Clear pricing in a field full of incumbents.",
      text: "Plans run from $50 to $1,000 every 30 days, with usage billed on top. It replaces Datadog, Grafana, Sentry and Axiom, and AI SRE startups and a batchmate chase the same buyers.",
      refs: ["Prices: Hobby $50", "Usage past the plan", "legacy tools it replaces", "AI SRE startups", "Same batch, overlapping product: Superlog"] },
  ],
};

// A short paragraph on what each company does, from the evidence. refs work as above.
window.TC_ABOUT = {
  ploy: { text: "Ploy turns a company's website into its growth engine: an AI platform that builds and runs the site and its marketing. It moves sites over from WordPress, Webflow, Framer and Wix. Plans run from free to $300 a month, with enterprise priced on request. A YC Spring 2026 company of 14 people, based in San Francisco and New York.",
    refs: ["Prices: Free $0", "moves sites over from", "Team size on YC: 14", "based in San Francisco and New York"] },
  sazabi: { text: "Sazabi is an AI-native observability platform for fast-moving engineering teams, pitched as Datadog for the AI era. It takes in a team's logs and investigates problems on its own. Plans run from $50 to $1,000 every 30 days, with usage billed on top. A YC Spring 2026 company of 10 people.",
    refs: ["legacy tools it replaces", "onboarded 35 teams", "Prices: Hobby $50", "Team size on YC: 10"] },
};
