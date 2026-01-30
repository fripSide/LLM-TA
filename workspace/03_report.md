# 密码安全用户研究 - Analysis Report

## Interview Results


### The Spectrum of Management Strategies: From Cognitive Patterns to Technological Offloading

Participants demonstrated a distinct dichotomy in their approach to password construction and storage, ranging from reliance on human memory to the adoption of specialized software. A significant portion of users employed cognitive strategies to maintain access, such as utilizing a single 'master password' across multiple sites, constructing passwords based on memorable patterns (e.g., combining words with years), or modifying a base password with predictable suffixes. For these users, the primary goal was memorability, often leading to insecure storage habits like writing credentials in digital notes or relying on browser autofill features. Conversely, a subset of participants adopted a technology-centric approach, offloading the cognitive burden to password managers. These users prioritized entropy over memorability, generating long, random character strings unique to every account. While this strategy significantly enhanced security by eliminating reuse, it introduced new dependencies, such as the critical need to secure the master password—sometimes via physical backups—and reliance on the software's availability. This theme highlights the fundamental trade-off users navigate between the convenience of memory-based access and the security of tool-assisted management.


**Supporting Evidence:**


> "就还是用我那个老密码呗，后面加个1或者2。如果是必须要大写字母，我就把首字母大写。" — P01


> "基本都是一个主密码变来变去。" — P01


> "像支付宝登录密码，其实和我淘宝密码是一样的，因为是一家的嘛。" — P01


> "所以我现在都把新改的密码写在手机备忘录里，不然根本记不住。" — P01


> "看情况。如果是重要的，比如工作账号... 如果是一次性的网站，就浏览器自动生成一个强密码" — P02


> "我会由两个常用的单词组合加上当前的年份。" — P02


> "先看 Chrome 浏览器有没有记住。如果记住了就直接填充。" — P02


> "我用 1Password 管理，里面记录了大概 350 多个条目。" — P03


> "生成 20 位随机字符，保存，填入。我根本不知道那个密码是啥。" — P03


> "每一个，我是说每一个账号，密码都不一样。因为全是随机生成的。" — P03


> "所以我把主密码设得巨长，而且记在了一张纸条上放在保险柜里，以防我失忆。" — P03





### Risk Perception and Tiered Security Models

User investment in password security was rarely uniform; instead, it was heavily influenced by a personal risk assessment that prioritized financial assets over data privacy. Participants frequently described a mental tiering system where banking and primary communication accounts (Tier 1) warranted strong, unique protection, while low-risk accounts like forums (Tier 3) were subject to intentional password reuse. In this mental model, the perceived value of the account dictated the security effort, with financial loss serving as the primary motivator for vigilance. However, this theme also revealed gaps in user risk perception. Some participants expressed a sense of invulnerability due to a lack of wealth, believing they were not targets for attackers. Others recognized the structural risks of the digital ecosystem, identifying email accounts as single points of failure that could trigger a domino effect of compromised identities. This suggests that while users apply a logical framework to security, their assessment of 'value' does not always align with the actual potential for data exploitation.


**Supporting Evidence:**


> "钱吧，肯定怕钱被转走。至于聊天记录啥的，也没啥见不得人的，不怕看。" — P01


> "但我感觉跟我没啥关系，我也没什么钱。" — P01


> "设计了分级的。T1 是银行、主邮箱、微信... T2 是京东、美团... T3 就是各种论坛" — P02


> "T3 就是各种论坛，基本全一样，丢了也无所谓。" — P02


> "主邮箱被盗。因为很多其他账号都能通过邮箱找回密码。一旦邮箱丢了，就像多米诺骨牌一样全完了。" — P02





### Friction, Fatigue, and the Desire for Seamless Authentication

A pervasive theme across the dataset was 'security fatigue,' where rigid security protocols conflicted with user experience, often leading to unsafe behaviors or service abandonment. Participants expressed strong frustration with mandatory password rotation and inconsistent composition rules (e.g., length limits), describing these requirements as 'security theater' that forced them into predictable behaviors like incrementing numbers. This friction caused some users to abandon account creation entirely or give up on accounts when recovery processes proved too cumbersome. Consequently, there was a strong preference for authentication methods that minimized cognitive load. Users overwhelmingly favored biometrics and SMS/OTP logins, not necessarily for their security benefits, but for their convenience and the elimination of memory requirements. This desire for a 'passwordless' experience extended to hopes for better operating system integration and the adoption of Passkeys, highlighting a user demand for security that is invisible and frictionless rather than intrusive.


**Supporting Evidence:**


> "反正现在都能手机号登录，密码基本也就是个摆设。" — P01


> "人脸识别我也开，主要是不是为了安全，是为了方便，不用输密码了嘛。" — P01


> "最后它说我账号被锁定了，让我找客服。我一气之下就注册了个新的，不登了。" — P01


> "最好就是不用密码，走哪里都刷脸。" — P01


> "我觉得太麻烦了，有时候为了看个文章还得注册，我就直接关了不看了。" — P01


> "定期更换是最愚蠢的策略... 我每次遇到这种强制要求都很反感" — P02


> "这只会逼着用户把密码改成 Password01, Password02... 只能被迫用一些规律性的变化。" — P02


> "就是像现在的 Passkey（通行密钥）那样吧。不需要密码，直接生物识别验证。" — P02


> "很多网站的密码规则太奇葩了... 限制长度不能超过16位... 限制长度是帮黑客爆破吗？" — P02


> "如果没有... 那就说明我没注册过，或者当时注册那个号太不重要我都没存。没存的话基本就放弃了" — P03


> "这种规则对真正的密码管理器用户很不友好。有时候生成的随机密码不符合它的规则（比如必须有大写），我还得手动调整。" — P03


> "定期更换也是，毫无意义的安全剧场。" — P03


> "每次听说我都会给朋友安利密码管理器，但由于上手门槛太高，他们基本都不用。" — P03


> "国内很多 APP 不支持标准的密码填充 API，导致还要手动切出去复制粘贴，体验极差。" — P03


> "希望操作系统层面能打通，不管是在 PC 浏览器还是手机 APP，都能一键识别并填充。" — P03





### Interpersonal Sharing and Reactive vs. Proactive Security Behaviors

This theme captures how users navigate the social aspects of credential sharing and their behavioral responses to security threats. Sharing passwords remained a common necessity, particularly for streaming services, but methods varied significantly in sophistication. While some users transmitted unencrypted passwords via messaging apps, others employed obfuscation techniques (e.g., retracting messages) or physical notes, and advanced users utilized secure sharing features within password managers. Regarding threat response, the data revealed a spectrum from apathy to proactive defense. Some users ignored security alerts or neglected to change passwords after breaches due to the inconvenience, while others adopted a 'reactive' stance, mass-updating credentials only after a confirmed incident. Conversely, a segment of 'proactive' users utilized tools like 'HaveIBeenPwned' and adopted Two-Factor Authentication (2FA)—ranging from hardware keys to authenticator apps—to preemptively secure their digital lives, despite the added friction.


**Supporting Evidence:**


> "我就申诉找回来了，也没改密码，太麻烦了。" — P01


> "视频会员经常借给朋友。我就直接微信发过去呗。" — P01


> "收到过，但我看了一眼，也不知道是真是假，就没管。" — P01


> "CSDN 泄露那次我就中招了。之后我就把所有重要账号密码全改了一遍。" — P02


> "现在看到那种大规模泄露的新闻，我会去 HaveIBeenPwned 查一下。" — P02


> "只要支持 2FA 的我都开。特别是 Google Authenticator... 虽然稍微麻烦点，但心里踏实。" — P02


> "死活想不起来，密保问题的答案也忘了。最后只能放弃，里面的照片估计也没了。" — P02


> "比如 Netflix 账号给家里人用。我是直接写在便签纸上贴在家里 iPad 背面。" — P02


> "线上发的话，发完我会撤回，或者分两段发。" — P02


> "我不用短信验证码，不安全。我用 YubiKey 这种硬件 Key，或者 Authy 这种 APP。" — P03


> "我用 1Password 的家庭共享功能... 绝对不通过微信发明文密码。" — P03






---

## Discussion








### RQ1: The Cognitive-Technological Divide in Credential Management

Our findings reveal that password management in daily life is not a monolithic practice but a spectrum defined by the user's willingness to offload cognitive burden to technology. We observed a distinct dichotomy between 'memory-reliant' users and 'tool-assisted' users (Theme 1). For the former, management is a cognitive exercise; they rely on pattern-based modifications (e.g., appending years) and ecosystem-based reuse to maintain accessibility. This aligns with classic HCI theories on bounded rationality, where users satisfice security to preserve cognitive resources. Conversely, tool-assisted users shift the security burden from memorability to system reliability, prioritizing entropy through password managers. However, this introduces new vulnerabilities, specifically the 'single point of failure' regarding the master password and the need for physical backups. Furthermore, management extends beyond storage to sharing (Theme 4). We found that social context dictates the method: low-stakes sharing (e.g., streaming accounts) often occurs via insecure channels like messaging apps, while high-stakes sharing utilizes obfuscation or secure tool features. This suggests that users view password management not just as a security task, but as a social negotiation between convenience, trust, and access.


### RQ2: Risk Perception and the 'Tiered' Mental Model

The importance users place on password security is heavily modulated by a personal, often financial-centric, risk assessment. Our analysis of Theme 2 indicates that users operate under a 'Tiered Security Model.' In this mental framework, accounts linked to direct financial assets (Tier 1) command high vigilance, whereas accounts perceived as having low intrinsic value (Tier 3, e.g., forums) are subject to intentional, pragmatic insecurity, such as password reuse. This finding challenges the 'security-by-default' approach, showing that users actively ration their security efforts based on perceived return on investment. However, a critical factor influencing this prioritization is the 'Invulnerability Misconception.' Users with lower financial assets often feel they are not targets, failing to recognize the structural value of their digital identity (e.g., email accounts) as a gateway for wider attacks. Thus, the primary factor influencing security behavior is not the technical strength of the system, but the user's subjective valuation of the data being protected.


### RQ3: Friction, Fatigue, and System-Induced Vulnerabilities

Users encounter significant problems not only from external threats but from the security mechanisms themselves. A dominant issue identified is 'Security Fatigue' (Theme 3), where rigid enforcement of policies—such as mandatory rotation and inconsistent composition rules—paradoxically degrades security. These mechanisms create friction that forces users into predictable behaviors (e.g., incrementing digits) or leads to 'Shadow Security' practices like writing passwords in digital notes. Beyond bad habits, this friction causes tangible service abandonment; users reported giving up on account creation or recovery processes that were too cognitively demanding. Additionally, the 'Reactive' nature of threat response (Theme 4) highlights a usability gap in current breach notification systems. Many users only address security issues post-incident because proactive tools (like 2FA or breach monitors) are perceived as adding unnecessary friction to the login flow. Consequently, the most pressing problem users face is the misalignment between security protocols and human workflow, where the 'safe' way is often the most unusable way.


### Implications: Toward Invisible and Integrated Authentication

The strong user preference for biometrics and the frustration with app-specific inconsistencies (Theme 3) point toward a critical design implication: the need for 'Invisible Security.' The desire for OS-level integration and Passkeys suggests that users are ready to abandon the knowledge-based authentication paradigm entirely. Future systems should prioritize reducing the 'interaction cost' of security. Rather than educating users to create better passwords—a strategy that fights against human cognitive limits—designers should focus on platform-level solutions that unify authentication across apps and browsers, effectively removing the user from the credential management loop.






---

## Notes

- `[CITE]` markers indicate where citations should be added
- Review each section for accuracy against your data