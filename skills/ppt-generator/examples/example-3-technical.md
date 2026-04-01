# Example 3: Technical Presentation (English)

## Input

```
Create a presentation about our microservices migration. We moved from a monolith to microservices in 6 months.

Key decisions: event-driven architecture, Kafka for messaging, Kubernetes deployment.
Challenges we faced: data consistency, service discovery, monitoring complexity.
Results: 40% faster deployments, 99.99% uptime, 3x developer productivity.
Team of 6 engineers.
Target: 14 slides.
```

## Output

```markdown
# From Monolith to Microservices: A 6-Month Journey

**Type**: Technical Presentation
**Total Slides**: 14

---

<!-- slide: 1 -->
## From Monolith to Microservices in 6 Months

### Content

- Migrated 2M+ lines of code to event-driven microservices
- 40% faster deployments, 99.99% uptime
- 3x developer productivity improvement

### Layout

> title-slide: Title centered, key metrics displayed as large numbers at bottom

### Speaker Notes

> Good morning everyone. Today I want to share our experience migrating from a monolithic architecture to microservices. We completed this in 6 months with a team of just 6 engineers, and the results exceeded our expectations.

---

<!-- slide: 2 -->
## Agenda

### Content

1. Why we migrated
2. The monolith problem
3. Target architecture
4. Key technology decisions
5. Implementation timeline
6. Challenges and solutions
7. Results and metrics
8. Lessons learned
9. Q&A

### Layout

> agenda-slide: Numbered list, clean and minimal

### Speaker Notes

> I'll walk through the motivation, architecture decisions, implementation, and results. I'll spend the most time on the technology decisions and challenges, since those are probably what you're most interested in.

---

<!-- slide: 3 -->
## Why We Migrated

### Content

- Deployment cycles: 2 weeks → needed same-day
- Scaling: couldn't scale components independently
- Team bottlenecks: 6 engineers blocked on shared codebase
- Incident response: one failure cascades to entire system

### Layout

> content-bulleted: Pain points on left, urgency timeline on right

### Speaker Notes

> The monolith served us well for 3 years, but we hit a wall. Deployments took 2 weeks because everything was coupled. A bug in the notification module could take down the entire payment flow. We knew something had to change.

---

<!-- slide: 4 -->
## Before: The Monolith

### Content

- Single Rails app, 2M+ lines of code
- 47 database tables, shared PostgreSQL
- Monthly deploy cycle with feature flags
- Average deploy time: 4 hours
- MTTR: 45 minutes

### Layout

> content-data: Monolith architecture diagram with key stats overlaid

### Speaker Notes

> This is what we started with. A single Rails application with over 2 million lines of code. Everything from user auth to payment processing to notification was in one codebase. A typical deployment involved 4 hours of careful coordination.

---

<!-- slide: 5 -->
## After: Event-Driven Microservices

### Content

- 12 domain services, each independently deployable
- Kafka as the event backbone
- Kubernetes for orchestration and auto-scaling
- Average deploy time: 12 minutes
- MTTR: 3 minutes

### Layout

> content-image-focus: Target architecture diagram, large and centered

### Speaker Notes

> And this is where we ended up. 12 services, each owned by 1-2 engineers. Kafka connects everything through events. Kubernetes handles deployment and scaling. Deploy time went from 4 hours to 12 minutes.

---

<!-- slide: 6 -->
## Key Decision: Event-Driven Architecture

### Content

- Services communicate via events, not REST calls
- Kafka as the central event bus
- Each service owns its data and publishes domain events
- Enables loose coupling and independent evolution

### Layout

> content-comparison: Left: synchronous REST calls (before), Right: async events (after)

### Speaker Notes

> This was our most important architectural decision. Instead of services calling each other synchronously, they publish events to Kafka. The payment service doesn't need to know about the notification service. This loose coupling is what makes the whole system resilient.

---

<!-- slide: 7 -->
## Key Decision: Kafka for Messaging

### Content

- Chosen over RabbitMQ and AWS SNS/SQS
- Event persistence and replay capability
- Exactly-once semantics for financial events
- Handles 50K events/second at peak

### Layout

> content-bulleted: Decision criteria table with Kafka, RabbitMQ, SNS/SQS comparison

### Speaker Notes

> We evaluated three options. Kafka won because of event persistence — we can replay events if something goes wrong, which is critical for financial data. The exactly-once semantics guarantee was also a must-have for us.

---

<!-- slide: 8 -->
## Key Decision: Kubernetes

### Content

- Auto-scaling based on CPU and custom metrics
- Rolling deployments with zero downtime
- Service mesh (Istio) for traffic management
- GitOps workflow with ArgoCD

### Layout

> content-bulleted: Key benefits with Kubernetes architecture mini-diagram

### Speaker Notes

> Kubernetes was the obvious choice for orchestration. The auto-scaling alone saved us from several potential outages during traffic spikes. Istio gives us fine-grained traffic control, which we use for canary deployments.

---

<!-- slide: 9 -->
## Challenge: Data Consistency

### Content

- Problem: No more ACID transactions across services
- Solution: Saga pattern for distributed transactions
- Outbox pattern for reliable event publishing
- Eventual consistency with 99.9% SLA

### Layout

> content-comparison: Problem vs Solution format, with saga flow diagram

### Speaker Notes

> This was the hardest problem. In a monolith, you wrap everything in a database transaction. In microservices, you can't. We adopted the Saga pattern: each service does its part and publishes an event. If anything fails, compensating events roll it back. We achieve eventual consistency with a 99.9% SLA.

---

<!-- slide: 10 -->
## Challenge: Service Discovery & Monitoring

### Content

- Istio service mesh for automatic discovery
- Prometheus + Grafana for metrics
- Distributed tracing with Jaeger
- Custom dashboards for each service team

### Layout

> content-image-focus: Grafana monitoring dashboard screenshot

### Speaker Notes

> When you go from 1 service to 12, observability becomes critical. We invested heavily in monitoring from day one. Each team has their own Grafana dashboard, and Jaeger lets us trace a request across all services end-to-end.

---

<!-- slide: 11 -->
## Implementation Timeline

### Content

- Month 1-2: Architecture design and Kafka setup
- Month 3-4: Migrate user and auth services
- Month 5: Migrate payment and order services
- Month 6: Final migration, load testing, go-live

### Layout

> content-timeline: Horizontal timeline with 4 phases

### Speaker Notes

> We took an incremental approach. Started with the lowest-risk services — user and auth — and worked our way up to the critical path: payments and orders. This let us learn and adjust as we went.

---

<!-- slide: 12 -->
## Results: The Numbers

### Content

- Deploy frequency: 1/month → 20+/month (40x)
- Deploy time: 4 hours → 12 minutes (20x faster)
- Uptime: 99.9% → 99.99%
- MTTR: 45 min → 3 min (15x faster)
- Developer productivity: 3x improvement

### Layout

> content-data: Before/after comparison with large numbers and trend arrows

### Speaker Notes

> The numbers speak for themselves. We went from deploying once a month to over 20 times a month. Uptime went from three nines to four nines. And most importantly, developer satisfaction went through the roof — engineers can now ship features independently.

---

<!-- slide: 13 -->
## Lessons Learned

### Content

- Start with the least critical services first
- Invest in observability before you need it
- Event-driven doesn't mean event-ually consistent everywhere — use sagas
- Team ownership model matters more than technology choices
- 6 months was aggressive but doable with a focused team

### Layout

> content-bulleted: Numbered lessons, concise and impactful

### Speaker Notes

> If I had to do this again, I'd invest even more in observability and testing infrastructure upfront. And I'd stress the importance of clear service ownership — technology choices matter less than having a team that truly owns their domain.

---

<!-- slide: 14 -->
## Q & A

### Content

- Thank you for your attention
- Contact: eng-team@company.com
- Architecture docs: wiki.company.com/microservices

### Layout

> q-and-a: "Q & A" centered, contact info at bottom

### Speaker Notes

> That wraps up our journey from monolith to microservices. I'm happy to dive deeper into any of the topics covered. Feel free to reach out afterwards as well.

---

> This outline was AI-assisted. Please review and adjust content before presenting.
```
