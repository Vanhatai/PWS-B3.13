class Tag:
    def __init__(self, tag="html", klass=None, is_single=False, output="", **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.output = output

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():   # именованные аргументы с нижним подчёркиванием превратить в атрибуты с дефисом 
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self
        
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(f'{attribute}="{value}"')
        attrs = " ".join(attrs)

        if self.children:
            opening = f"<{self.tag} {attrs}>"
            if not attrs:
                opening = f"<{self.tag}>"
            internal = f"{self.text}"
            for child in self.children:
                internal += str(child)
            ending = f"</{self.tag}>"
            return opening + "\n" + internal + "\n" + ending
        
        if self.is_single:
            return f'<{self.tag}{" " + attrs if attrs else ""}/>'
        else:
            return f'<{self.tag}{" " + attrs if attrs else ""}>{self.text}</{self.tag}>'

    def __add__(self, other):
        self.children.append(other)
        return self

class TopLevelTag(Tag): # не заданы четки условия, что такое TopLevelTag, например, <div> со вложенным <p> - просто Tag
    pass                # итого используем просто Tag с вложениями или без

class HTML(Tag):
    def __exit__(self, *args):
        if self.output:
            with open(self.output, 'w') as out_file:
                print(str(self), file=out_file)
        else:
            print(str(self))
# ===========

with HTML(output="test.html") as doc:
# with HTML() as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body
