================
Design Decisions
================

If you're interested, here's some reasoning behind why flask transmute
works the way it does.

----------------------------------
A separate object from a flask app
----------------------------------

Transmute was designed with flask in mind, but the final goal has been
expanded as transmute's function -> api spec generation does not need to be framework-specific.
In the future, support for other frameworks such as Tornado are planned.

Driven by the need for a framework-agnostic design, it made sense to create a transmute
object, then apply that to a particular framework.
