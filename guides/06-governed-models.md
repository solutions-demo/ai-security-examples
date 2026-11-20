# 6. Governed AI models

Detect models pulled outside governance (Shadow AI), block them, and bring them under a governed project.

## 1. Set up an ungoverned "shadow" surface

Create repositories outside your evaluation project, to stand in for unmonitored AI usage:

1. Go to **All Projects → Administration → Repositories → Create Repository → Remote → HuggingFace** and
   name it `shadow-model-repo`. Enable **Xray indexing** while creating it.
2. Create a **local Docker** repository named `shadow-model-docker-repo`.

## 2. Give the developer user access

These repositories sit outside the developer user's project, so grant access explicitly:

1. Go to **All Projects → Administration → User Management → Permissions → New Permission**.
2. Under **Repositories**, select `shadow-model-repo` and `shadow-model-docker-repo`. Under **Users**, add
   the developer user.
3. Save.

## 3. Download a model through the ungoverned repository

With a Python environment available, run:

```bash
jf hf download google/flan-t5-small --repo-key=shadow-model-repo --server-id=<YOUR-SERVER>
```

Because the model came through a repository that no governed project owns, it's recorded as a shadow
model.

> [!TIP]
> Direct downloads from Hugging Face can also be intercepted and routed through Artifactory with the
> Package Traffic Controller.

## 4. Find and block it

1. Open **AI Security → Shadow AI**.
2. Find `google/flan-t5-small`, marked **Unmanaged**, and open it.
3. On the **Found At** tab, find `shadow-model-repo` and click **Block**, or **Block everywhere**.

## 5. Confirm the block

Blocking takes a few minutes and changes the status to **Managed**. Clear the local cache and try the
download again:

```bash
rm -rf ~/.cache/huggingface/hub/models--google--flan-t5-small
jf hf download google/flan-t5-small --repo-key=shadow-model-repo --server-id=<YOUR-SERVER>
```

The download should now be refused.

## 6. Detect a model inside a container image

This uses the `jfrog-hf-docker-demo` sample from [jfrog/JFrogMLExamples](https://github.com/jfrog/JFrogMLExamples).

1. Build the image with the model baked in:

   ```bash
   cd jfrog-hf-docker-demo/
   ./build-with-local-model.sh
   ```

2. Push it to the shadow Docker repository:

   ```bash
   export ARTIFACTORY_URL=<YOUR-ARTIFACTORY-URL>
   export ARTIFACTORY_REPO=shadow-model-docker-repo
   ./push_to_jfrog.sh
   ```

   If the script fails to authenticate, push with the JFrog CLI instead:

   ```bash
   jf docker push <your-instance>.jfrog.io/shadow-model-docker-repo/jfrog-hf-demo:latest --server-id <YOUR-SERVER>
   ```

3. Open **Shadow AI** and check `google/flan-t5-small` again. It now shows **Partially Managed**, with the
   Docker repository and image path listed under **Found At**.

## 7. Bring it under governance

To govern the model rather than block it:

1. Associate both shadow repositories with your evaluation project.
2. Go to **AI Security → Marketplace → Models**, search for `flan-t5-small`, and add it to your registry.

---

**Previous:** [← 5. Agent skills](05-agent-skills.md)
