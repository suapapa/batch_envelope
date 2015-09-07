# batch_envelope

print input address to envelope for snail mail.

# todo

- address input
- execute template
- print with lpr
- print on GCP

# reference
Convert SVG to PDF and printit.

    $ inkscape my_graphic.svg --export-text-to-path \
    --export-pdf=my_graphic.pdf
    $ lpr -o landscape test.pdf

* [GCP CUPS Connector](https://github.com/google/cups-connector)
