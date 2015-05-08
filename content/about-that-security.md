Title: About that security
Date: 2015-05-07 21:17
Author: Ingmar Steen
Tags: security
Status: draft

The context of this rant is [a conversation with Tracy Osborn](http://importpython.com/blog/post/conversation-tracy-osborn-author-hellowebapp) on the importpython blog.

On the surface, the linked article tells an endearing tale about a woman whom, after several setbacks, one of them related to the schism between web design and programming, manages to launch a successful startup that helps web designers to bring their designs to life. Well, I assume it's successful as they're talking about it. 

All in all a pretty inspiring interview for people that want to code but for whatever reason can't follow the traditional path.

However... There's one bit that really irked me. And I'm probably dragging this way out of context. And perhaps I'm exaggerating. And maybe I'm just plain wrong. And... Well, let's just look at the quote (question in bold, answer in italics):

> **Computer science fundamentals plays a key role in designing a good software architecture. At what point does a designer who launched his or her own site / web app say OK! I need expert help now?**
>
> *Most computer science fundamentals and best practices can be ignored for the beginner, in my opinion, as long as it doesn't break security. As a designer builds up their website/web app, I believe they'll stumble into best practices and principles on their own.*

And that describes exactly what is wrong with a large part of the development community and startups in particular: how are you supposed to know what is and what isn't a secure thing to do? Application security (both online and offline) is such an intricate matter that you should start every new project by investigating what the security requirements will be. Especially in today's world where everything's connected and particularly when creating a web application. Nothing screams *attack surface* like a new web application by an inexperienced developer.

Knowing about how to properly design an application helps identifying potential security pitfalls. Everybody knows you shouldn't store passwords plain text in a database, everybody hashes passwords.

But how do you properly salt a password? Where do you store that salt? What kind of hashing algorithm should you use? And that's just storing and verifying a password. Now extend that with preventing SQL injection, cross site scripting (XSS) and local file inclusion (LFI). And even those just cover the basics. Do you use existing libraries to implement your requirements? Which one do you pick? How do you know it's good enough for your use case?

It's almost impossible to prevent things from going south very quickly without knowing where you're headed. If there's anything you're going to learn before creating your new website or application, please learn about security. And, following a solid set of best practices and principles helps with that a lot.

Now, I'm probably not being fair to Tracy Osborn... I've never met her,  spoken to her or even heard about her or her HelloWebApp project before and I have no idea what her actual views on security are.

However, the proper answer to the question the interviewer asked should always be: *right at the beginning of your project*. Security first! 

*PS. Tracy: If you're reading this, I am truly sorry about my terrible webdesign. ;-)*