# Walkthrough

## Intro

Let's take a quick look at some kubernetes basics and how traefik can make exposing a service quick and easy.

All of the provided files are populated with a domain owned by the author. In order to follow along, you'd have to start by changing to a domain in your control that points to your k8s cluster.

We're going to be running several commands, so I'm going to start by creating a few aliases to make things go quicker.

```
alias k='kubectl'
alias kn='kubectl -n $NS'
alias knd='kubectl -n $NS describe'
alias kng='kubectl -n $NS get'
alias kga='kubectl get --all-namespaces'
```

This sets us up to rapidly look for and inspect various kubernetes resources.

## Short k3s Addons Look

One of the first things to do when exploring any new k8s cluster is to inspect the available namespaces.

```
k get ns
```

The available namespaces will depend on the cluster setup. If you've chosen to use k3s as your k8s distribution, you'll have a `kube-system` namespace automatically. This is where k3s installs addons that provide basic cluster services. We can explore what comes installed by default by looking at some of the deploys.

```
export NS=kube-system
kn get deploy
```

There's a `coredns` service that provides DNS functionality to the cluster as a whole. There's also a `local-path-provisioner` to handle local storage needs and a `metric-server` that reports k8s specific metrics. Finally, there's `traefik`, the Ingress provider for the cluster.

## Traefik Dashboard

Before we dive into using traefik, let's take a look at the dashboard that comes with it to get an overview of what it's providing. First, identify the service providing the dashboard.
```
kn get svc
```

There should be a `traefik-dashboard` service, and if the default configuration is used, it'll be serving over port 9000. Let's forward that service so we can access it on localhost.

```
kn port-forward svc/traefik-dashboard 9000:9000
```

You should be able to view the service at `http://localhost:9000/dashboard/`. The ending `/dashboard/` is required and mentioned in the traefik documentation.

The homepage shows the entrypoints being served on various ports and a health status of all the routers and enabled features. Clicking into the various sections allows for viewing more detail about routers and their configuration.


## Traefik Hands On

It's more fun to set up a brand new service and see how things work, so let's try out the provided demo example from traefik.

### Example App Creation

First, create a namespace, deploy, and service for the example app.
```
k apply -f 01-deploy.yaml
```

We could check on the app using the previous `port-forward` command for `kubectl` and use the example app's port of 8080, but in the interest of time, let's move on.

### Certificate Request

Next up, create a Certificate to secure the app. This leverages an installation of cert-manager that is configured to work with traefik. Behind the scenes, it will automatically create an ingress to respond to an HTTP challenge used to verify we own the domain that is in our certificate. This is the default verification method for requesting using Let's Encrypt.

```
k apply -f 03-cert-patch.yaml
```

If we are lucky and paying attention, we might be able to catch the router being create temporarily to respond to the challenge, but it is often so fast that it's already done before we can even see it. We'll check on the status of the Certificate before moving forward.

```
kn get cert
```

We started by requesting a Certificate from a staging endpoint with Let's Encrypt. This is a good practice to follow, as it makes sure all of the required network communication and DNS are in place before we request a production certificate. If our certificate shows a `READY` status of `True`, we're ready to proceed. We'll patch our prior Certificate resource to change to use the production endpoint.

```
kn patch cert whoami --type=json --patch-file=03-cert-patch.yaml
```

### IngressRoute

Once the production cert shows as ready, we can create our IngressRoute.

```
k apply -f 04-ingressroute.yaml
```

We should be able to verify our new router in the traefik dashboard, and we can see the shield representing TLS. If we visit our domain, we'll see our example app!


## Traefik Middleware

That covers the basics, but there's a lot of other functionality that can be unlocked with Middleware. We'll take a quick look at two common use cases.

### HTTPS Redirect

While we went ahead and setup the example app to respond over HTTPS, if we tried to visit the site on HTTP, we'd end up gettting an error. We'd prefer visitors to our site get automatically redirected.

To handle a redirect, we create a redirect middleware, and we apply that middleware to a new IngressRoute that's pointed to traefik's `web` entrypoint rather than `websecure`.

```
k apply -f 05-https-redirect.yaml
```

If we visit the example app on HTTP, we'll now be redirect to the HTTPS version.

### Basic Auth

The example app isn't much, but maybe we don't want to expose it to the world. Introducing basic auth is a quick way to put a username and password in front of visitors.

To start, we'll create a k8s secret that will store the allowed users. We'll use a script that calls the Apache tool `htpasswd` to generate a file with a user and hashed password that will serve as the data in the secret.

```
> ./06-basic-auth-user.sh
Adding password for user test
secret/whoami-users created
```

Now that the secret exists, we can create the middleware that will use it.

```
k apply -f 07-basic-auth-middleware.yaml
```

Finally, we'll patch our IngressRoute on the `websecure` entrypoing to use the new middleware.

```
kn patch ingressroute whoami --type=json --patch-file=08-basic-auth-patch.yaml
```

Visiting our site should now prompt a username and password. The script defaults to username `test` and password `test`. It's super secure.
