###PROBLEM
- diagrams in GIF, JPEG, PNG format-s are chronically phugly (when zooming them in/out)
- SVG diagrams are beautiful (non-phugly), but
- github at the moment does **not** permit/support using/including/linking to SVG files **stored in your github repo** in your github markup files (for example README.md)

###SOLUTION
- create a SVG file and store it on an external fileserver, like for example amazon s3
- in your github markdown file (for example README.md) use the `<img>` HTML element with the `src` attribute set to the SVG file amazon s3 URL: `<img src="https://s3-ap-southeast-2.amazonaws.com/atlasoflivingaustralia.github.io/ala-hub/gfx/architecture-01.dot.svg"></img>` 

_EXAMPLE (click the image bellow and/or zoom in/out this page to see that this is REALLY a GENUINE SVG diagram):_

<img src="https://s3-ap-southeast-2.amazonaws.com/atlasoflivingaustralia.github.io/ala-hub/gfx/architecture-01.dot.svg"></img>

---
NOTES: https://github.com/mbohun/mbohun_graph-experiments/tree/master/github-svg-test
