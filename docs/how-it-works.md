# How it works

Wingtip Vortex computes the wing vapor: for every lifting part it holds a grid of points over the planform, each with a vapor density from 0 to 1 and the side of the part the suction is on. Each frame it hands this mod the parts carrying vapor. Everything below is how that becomes two clouds.

The code is in [`Source/VaporVolume.cs`](../Source/VaporVolume.cs).

<br>

## The shape being drawn

Waterfall's volumetric shader draws a tube: a cylinder whose radius can change linearly along its length (a taper) and bulge in the middle. The mod lays one tube along each wing's span, root to tip, flattened so that it is wide along the airflow and thin off the wing.

So the whole job is choosing, for each side of the craft, where the tube's two ends are, how wide it is at each, and how tall.

<br>

## Measuring the vapor

* **Directions.** "Along the flow" is the direction the air moves past the craft. "Off the wing" comes from the suction side of the parts carrying vapor. "Across" is the span, square to both
* **Strips.** The vapor is sorted into 24 strips across the span. Each strip records how much vapor it holds, where along the flow it starts and ends, how dense it is, and how high the wing surface is there
* **Where a strip ends.** A strip's vapor is followed aft from its start until a gap of 1.5 m. A tail well behind the wing is past that gap, so it does not stretch the wing's cloud back to itself

<br>

## Choosing which strips are the wing

On each side, the mod finds the straight line that the most vapor starts on, and keeps only the strips that start close to it (within 0.6 m, or 15% of the vapor's mean chord if that is more). A strake ahead of the wing or a tail behind it starts well off that line and is left out.

The line from the last frame is kept unless a new one has at least 10% more vapor on it, so strips do not flip in and out from frame to frame.

<br>

## Fitting the cloud

* **Sweep, taper and height.** Straight lines are fitted through the kept strips for the vapor's mid-chord position, its half-chord and the wing's height, each against span. Read off at the inner and outer ends, they give the tube's root and tip
* **Width.** The tube is 1.15 times as wide as the vapor along the flow
* **Height.** It grows with the chord and with the square root of the vapor's density, scaled by the Thickness setting, and is capped at 3 m and at 0.45 of the tube's half-width
* **Front edge.** The tube's front, as drawn, is a little curved and is cut square to its own axis, not to the airflow. So after the first fit the axis is slid and turned, in three passes, until the drawn front lies along where the vapor starts. It ends up slightly ahead of the leading edge mid-span and slightly behind it at the root and tip
* **Over the fuselage.** When both sides carry vapor and neither starts more than 2.5 m out, each tube runs 1 m past the centreline and fades in over that stretch, so the two add up to one cloud there

<br>

## Drawing it

* The fit is followed with a 0.15 s lag, so the cloud moves smoothly
* Brightness goes with the vapor's density and with how much wing is condensing (full at 1.5 m² of dense vapor), times Wingtip Vortex's vapor intensity setting
* The tint follows daylight, as the puffs do
* The shader adds light and does its own depth test against the scene, so the cloud is cut cleanly by the airframe but cannot darken what is behind it
