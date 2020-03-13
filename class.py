class Tag:
    def __init__(self, tag, src = None, id = None, klass = None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.klass = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.src = ""
        self.id = ""

        if klass is not None:
            self.attributes['class'] = ' '.join(klass)

        if src is not None:
            self.attributes['src'] = ''.join(src)

        if id is not None:
            self.attributes['id'] = ''.join(id)

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        

    def __str__(self):
        attrs = [] 
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if len(self.children) > 0: 
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child) 
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else: 
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )

class HTML:
    def __init__(self, output=None, is_single=False, **kwargs):
        self.html = ""
        self.output = None
        self.attributes = {}
        self.children = []
        self.is_single = is_single
    
    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, type, value, traceback):
        if self.output is not None:
            with open("my_file.txt" , "w") as f:
                f.write(str(self))
        else:
            print(self)


    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html
        


class TopLevelTag:
    def __init__(self, taga, is_single=False):
        self.taga = taga
        self.attributes = {}
        self.children = []
    
    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

    def __str__(self): 
        html = "<%s>\n" % self.taga
        for child in self.children:
            html += str(child)
        html += "\n</%s>" % self.taga
        return html


if __name__ == "__main__":
    with HTML(output=None) as doc:
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

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

        doc += body
