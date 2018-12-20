# parts.horse

A website providing information about various electrical components.

Features overview:

* No images, only text.
* HTML _and_ plain-text variants of all pages.
* CLI-friendly: actively tested with via `curl`, `w3m`.
* Search functionality: it's not great, but it exists.

**NOTE:** Unicode support is required for the pages to render correctly.

## HTML vs plain-text

At the moment, if the `Accepts` header is absent or does not include
`text/html`, it will return text-only.

In the future certain browsers will be special-cased to get HTML (e.g. ELinks).

## Dependencies

* Python3
* CherryPy
* Jinja2

## Development

(TODO: Link to something explaining how to set up a venv.)

Create and activate a Python3 virtual environment (venv), then:

```
$ pip3 install -r requirements.txt
$ ./app.py
```

## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/duckinator/parts.horse.

## License

The code is available as open source under the terms of the
[MIT License](https://opensource.org/licenses/MIT).
