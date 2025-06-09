## General questions

**These questions are straightforward to answer.**

- When was Nederlandse Spoorwegen (NS) founded?
    - NS was founded in 1938
- How many scheduled domestic trains does NS run per day, and how many passengers do they serve?
    - NS runs 4,800 scheduled domestic trains a day, serving 1.1 million passengers

## Questions about travelling with NS

**The questions below request the chatbot to synthesize information, look at different documents at once or to perform comparisons based on tables.**

- I need to take my bicycle on the train. Is this always possible, and what are the costs involved?
    - The document mentions about an off-peak bicycle ticket which costs €7.50.
- What are the main differences between a personal OV-chipkaart and an anonymous OV-chipkaart, especially concerning loss or theft?
    - A personal OV-chipkaart can be blocked when lost or stolen (after 24 hours) and allows for balance refunds after loss or theft, while an anonymous OV-chipkaart cannot be blocked and does not offer balance refunds.
- My train journey was delayed. How can I request a refund for the delay, and what information might I need?
    - via your online 'Mijn NS’

### Questions about train disruptions

**Only the agent-based chatbot should give information about disruptions.**

- Is there any train disruption in Enschede?
    - There are no disruptions in Enschede.
- Please let me know if there are train disruptions in Amsterdam.
    - Disruption on the route Amsterdam - Haarlem of 45 minutes due to a broken down train
- Give me details about train disruptions in London.
    - It should state that the tool has information only about disruptions from stations in the Netherlands.

### Questions about travelling with NS and train disruptions to highlight the orchestration

**Only the agent-based chatbot should give information about disruptions, but both should give details about refunding.**

- I want to take a train from Eindhoven in 15 minutes and I have already bought a ticket. Is there any train disruption? If so, how can I request a refund?
    - The chatbot is expected to mention about a disruption from Eindhoven to Venlo which led to a delay of approximately 287 minutes (nearly 5 hours) due to a collision and then to give details.
- I want to take a train from Enschede in 15 minutes and I have already bought a ticket. Is there any train disruption? If there is a disruption, let me know how can I get a refund.
    - It should state that there are no disruptions and mention about refund policies in the event they do occur. This two-part answer emphasizes the orchestration, as the second part of the answer is related to the disruption status.

### Out of scope questions

**No chatbot should have the answer to the questions below.**

- Is there any train disruption in Germany?
- Can you recommend a good Italian restaurant near Utrecht Centraal Station?
- Who is the president of the United States of America?
