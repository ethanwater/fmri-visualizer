# Research to Determine Correlation Between fMRI Simulations and User Response to Content

### Debrief
META's research team has recently released TRIBEv2, a multi-modal brain encoder to simulate a zero-shot fMRI to media (visual, audio, and textual). Their goal is to predict how the average population will respond to any form of content.

My hypothesis is that the fMRI simulations can lead to a more in-depth and accurate prediction of how a user may act with said content- these metrics include but are not limited to:
- user retention
- user drop off times
- user like times
- negative or positive visual stimuli
- negative or positive audio stimuli
- ...

### The System
Our system would be mid-modal utilizing both a brain encoder model (fMRI sims) and a visual stimuli model (video comprehension). Since both models are time-aware we can overlap the two and make powerful insights about when the issue was caused, where it was caused (in the brain), what it was that caused it, and how to revise it. If the results are as meaningful as i believe they will be then this will be an invaluable tool for all content creators in the world. The following is a high-level visual of the pipeline:

*input*
media -> brain encoder -> fMRI simulations 
media -> video encoder -> visual landmarks

*output*
Predictive Report and Editable Actions



### Challenges
There are some minor and major challenges that we'd have to face in this project:

**TRIBE v2 is NonCommercial**  
This means that we would need to engineer our own fMRI brain encoder. This gives us both full independent control, ability to fine tune, and only process what is necessary. However, this will be at the cost of development time and resources. 

**Populations, Subcultures, and Independent Personalities** - What unsettles one group may comfort another. Social media has undeniably amplified the many subcultures that make our society today and each group has their own traits, quirks, likes, and dislikes. No doubt this would apply to how these subcultures think as well. In the EDM scene and overwhelming level of activation in the Somamotor Network may be a positive thing whereas in the Meditation scene it may be a negative - these things matter. This is really just as cool (if not cooler) and can be a seperate study on it's own.


### The Goal
The goal is to provided a tool to independent creators that is comparable, if not better, than current neuroscience marketing agencies that exist today.

**The Secret Goal**
To compile a massive dataset that can map the independent traits of subcultures to fMRI encodings. AKA - we know which BOLD signals in which segments are good or bad depending on the target audience.

