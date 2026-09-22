# TrueGauge-Fuel-Detection-
A retrofit-viable, sensorless-first vehicle energy integrity indicator proposal for fuel adulteration and EV charging integrity — formal model, patent-landscape review, 14-country enforcement survey, and runnable notebooks. Preprint / design study, no prototype built yet. DOI: 10.5281/zenodo.22674618
The one-sentence version

Your car has no idea if the fuel you just put in it (or the electricity you just charged it with) is genuine — this paper is a proposal for how it could find out, using information the car already has.

The problem, explained simply

When you fill your tank, the pump shows you a price and a quantity. It doesn't tell you if the fuel has been mixed with cheaper, harmful stuff — a real and common practice in many countries called fuel adulteration. The same trust problem shows up with electric vehicles too: charging stations don't always bill you for exactly what they deliver, and poor-quality power can quietly damage your battery.

This isn't rare. The paper found real, documented cases — court rulings, government fines, regulator crackdowns — in at least 14 countries over the last 5 years. People genuinely lose money and damage their engines because of this.

What the paper actually proposes

A way for a car to grade the fuel, it just received (Good / Caution / Poor) using signals the car's computer already collects — no expensive new sensor required. The same idea is extended to EV charging, checking whether you were billed fairly and whether the power quality was safe for your battery.

A few things make this proposal careful rather than just hopeful:

It checks against real laws, not made-up rules. The same reading is judged differently in India vs. Europe, because it's compared against each country's actual legal fuel standards.
It doesn't jump to conclusions. A reading starts as "still checking" and only becomes "confirmed" after enough data comes in — so the car doesn't cry wolf.
It checked what already exists. The paper researched existing patents from GM, Ford, Volkswagen, Audi, and Bosch before proposing anything — and found Volkswagen already patented something similar just 10 months earlier. Instead of ignoring that, the paper explains exactly how this idea is different.
It asked "who would actually want this?" — and the honest answer wasn't individual drivers. It was insurance companies and vehicle fleets, who already have the right equipment and the biggest financial reason to care.
What the paper does NOT claim

This is a proposal and a feasibility study — not a finished, tested product.

No prototype has been built.
No real-world accuracy has been measured.
Nothing in this paper has been tried on a real car yet.

The paper is upfront about this everywhere it matters, and lays out exactly what would need to happen next to turn the idea into something real (building a test dataset, running a pilot, and checking it doesn't conflict with existing patents).

Why this topic, and who wrote it

Written by Rohit Joshi, a doctoral researcher at the European Institute of Management & Technology (EIMT), alongside a day job in the automotive industry. The idea started from a simple, everyday frustration: standing at a petrol pump with no way to know what you're actually getting.

Want to see it in action?

This repository also includes visual demos (a phone-app mockup, a dashboard concept, runnable notebooks) that show what this idea might look like if it were ever built — see the main for those.README.md

How to read the full paper

Open like any PDF. It's written in a formal academic style (equations, tables, citations) — if you just want the gist, this page is that gist.TrueGauge-EII-IEEE-format.pdf
