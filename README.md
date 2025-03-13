# drumdown

A markdown-inspired language for drum notation / generation.

## What can i do with this?

* Define songs as an ASCII document using the drumdown language
* Generate MIDI out of your document

There's no formal spec (other than the parser code) but you can look at the examples to get the hang of it

Currently supports kick drum, hat (open, closed), ride, cymbals, snare (accents, ghost notes, flams). So far the parser only understands 16th note-based grids.

## Future vision

* Filters: 
  * Ability to configure playing style
    * Accenting snare + hat on backbeats
    * Hat upstrokes vs downstrokes
  * Humanization
    * Timing
    * Velocity
* Configuration:
  * Different kinds of note maps
* Support other subdivisions (triplets!)
* Support crescendos
* Support more instruments: differentate between tom 1, tom 2, tom 3, etc
* Create a bigger library of example songs

See [ROADMAP.todo](./ROADMAP.todo) for more concrete next steps
