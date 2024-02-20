### Analyze, choose, and justify the appropriate resource option for deploying the app.

**Analysis**

* **Azure Virtual Machines (VMs)**
    * **Costs:** VMs offer granular control over hardware. Potential for cost optimization but with administration overhead.
    * **Scalability:** Can be scaled manually, offering flexibility but requiring intervention.
    * **Availability:** Increased uptime achievable with availability sets/zones, but you manage redundancy.
    * **Workflow:** Full OS-level administration required (patching, updates, dependencies).

* **Azure App Service**
    * **Costs:** Pay for an App Service Plan (defined resources). Scaling features help control costs.
    * **Scalability:** Easy scaling up/down, out/in (manual or rule-based).
    * **Availability:** Built-in load balancing, redundancy. Reduced admin overhead due to Microsoft-managed updates.
    * **Workflow:** Focus on code and app configuration, not the underlying OS.

**Choice: Azure App Service**

**Justification**

The CMS with Python/Flask aligns best with App Service due to:

* **Simplified Management:** Less overhead by avoiding full VM setup.
* **Cost-Effectiveness:** App Service plans match needs, scaling keeps costs aligned with usage.

### Assess app changes that would change decision.

Factors that might favor a VM:

* **Heavy Customization Needs:** Strict OS-level control or unusual software requirements.
* **Existing on-premises Hybrid Model:**  A VM might be a necessity for tight integration.
* **Complex, Non-Web Workloads:**  If the CMS heavily involves background processing or highly compute-intensive tasks alongside the web app.

### My app (available until Feb 27)
[Article CMS](https://udacity-article-cms.azurewebsites.ne)