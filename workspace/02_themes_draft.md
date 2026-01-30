# 密码安全用户研究 - 主题分析

> 以下是基于已选编码生成的初步主题。
> 您可以：移动编码到其他主题、修改主题名称、合并或拆分主题。
> **注意**: 请勿修改 `<!-- THEME_ID: ... -->` 和 `<!-- CODE_ID: ... -->` 注释。


### Cognitive Coping Mechanisms vs. Technological Offloading
<!-- THEME_ID: T01 -->
This theme explores the fundamental strategies users employ to handle the cognitive load of password management, addressing the research question regarding how users manage passwords in daily life. The data reveals a dichotomy between users who rely on internal cognitive heuristics and those who offload the burden to external tools. Many participants utilize mental shortcuts, such as reusing a master password for low-risk accounts or applying predictable transformation patterns (e.g., appending dates) to satisfy system requirements without true memorization. Conversely, a segment of users has transitioned to dedicated password managers, allowing for the generation of long, random strings that prioritize entropy over memorability. However, this transition is not universal; some users rely on unencrypted digital notes or physical paper as a middle-ground solution, while others express a belief that secure tools are too complex to adopt, highlighting a barrier to technological offloading.


- **CC_002**: A heuristic strategy where users...
  - _"就还是用我那个老密码呗，后面加个1或者2。如果是必须要大写字母，我就把首字母大写。"_ (P01)
  <!-- CODE_ID: CC_002 -->

- **CC_003**: The intentional use of a...
  - _"反正我记不住那么多密码，基本都是一个主密码变来变去。"_ (P01)
  <!-- CODE_ID: CC_003 -->

- **CC_005**: The reliance on unencrypted, external...
  - _"所以我现在都把新改的密码写在手机备忘录里，不然根本记不住。"_ (P01)
  <!-- CODE_ID: CC_005 -->

- **CC_009**: The use of dedicated software...
  - _"先看 Chrome 浏览器有没有记住。如果记住了就直接填充。"_ (P02)
  <!-- CODE_ID: CC_009 -->

- **CC_012**: The strategy of generating long...
  - _"生成 20 位随机字符，保存，填入。"_ (P03)
  <!-- CODE_ID: CC_012 -->

- **CC_020**: The belief that secure tools...
  - _"但由于上手门槛太高，他们基本都不用。"_ (P03)
  <!-- CODE_ID: CC_020 -->



### Risk Perception and the Tiered Valuation of Digital Assets
<!-- THEME_ID: T02 -->
This theme addresses the factors influencing users' attention to security, specifically how risk perception dictates behavior. Participants do not apply a uniform security standard across their digital lives; instead, they engage in a tiered classification of accounts based on perceived asset value. Financial accounts trigger high-priority security behaviors, while other services are often treated with negligence due to an 'optimism bias'—the belief that one is unlikely to be targeted. However, there is a counter-narrative where awareness of the 'domino effect' (where a compromised email leads to total identity loss) drives heightened vigilance. This theme also captures reactive behaviors, such as using third-party tools to check for leaks, demonstrating that user attention is often event-driven rather than proactive.


- **CC_001**: The practice of classifying accounts...
  - _"银行卡那是6位数字密码，那个肯定不一样... 其他的网站，只要不是很重要的，我就随便设个简单的。"_ (P01)
  <!-- CODE_ID: CC_001 -->

- **CC_015**: The prioritization of security behaviors...
  - _"钱吧，肯定怕钱被转走。至于聊天记录啥的，也没啥见不得人的，不怕看。"_ (P01)
  <!-- CODE_ID: CC_015 -->

- **CC_016**: The cognitive bias where users...
  - _"听说过啊，新闻里老说。但我感觉跟我没啥关系，我也没什么钱。"_ (P01)
  <!-- CODE_ID: CC_016 -->

- **CC_017**: The awareness that compromising a...
  - _"主邮箱被盗。因为很多其他账号都能通过邮箱找回密码。一旦邮箱丢了，就像多米诺骨牌一样全完了。"_ (P02)
  <!-- CODE_ID: CC_017 -->

- **CC_018**: The active use of third-party...
  - _"现在看到那种大规模泄露的新闻，我会去 HaveIBeenPwned 查一下。"_ (P02)
  <!-- CODE_ID: CC_018 -->



### Friction, Fatigue, and the Burden of Compliance
<!-- THEME_ID: T03 -->
Focusing on the problems users encounter, this theme highlights the negative consequences of rigid security policies and poor user experience (UX). The data suggests a widespread sense of 'security fatigue,' where users become exhausted by constant alerts or requirements, leading to indifference. Specific pain points include mandatory periodic password changes, which are viewed with skepticism as 'security theater,' and rigid complexity rules that conflict with user habits or password managers. This friction has tangible consequences: users report abandoning services entirely when authentication becomes too burdensome, facing permanent loss of access due to forgotten credentials, or struggling with poor software integration that forces manual data entry. These findings suggest that when security measures impede usability, users often bypass the system or disengage entirely.


- **CC_006**: A state of exhaustion or...
  - _"我就申诉找回来了，也没改密码，太麻烦了。"_ (P01)
  <!-- CODE_ID: CC_006 -->

- **CC_007**: The decision to stop using...
  - _"最后它说我账号被锁定了，让我找客服。我一气之下就注册了个新的，不登了。"_ (P01)
  <!-- CODE_ID: CC_007 -->

- **CC_010**: User frustration with and skepticism...
  - _"每次强制改密码，我都得想半天，改完了下次肯定忘。"_ (P01)
  <!-- CODE_ID: CC_010 -->

- **CC_011**: Dissatisfaction with inconsistent or rigid...
  - _"很多网站的密码规则太奇葩了，有的不让用特殊符号，有的限制长度... 这我就很不理解"_ (P02)
  <!-- CODE_ID: CC_011 -->

- **CC_014**: User difficulties arising from poor...
  - _"希望操作系统层面能打通，不管是在 PC 浏览器还是手机 APP，都能一键识别并填充。"_ (P03)
  <!-- CODE_ID: CC_014 -->

- **CC_019**: The permanent loss of access...
  - _"死活想不起来，密保问题的答案也忘了。最后只能放弃，里面的照片估计也没了。"_ (P02)
  <!-- CODE_ID: CC_019 -->



### Evolving Authentication Preferences and Social Behaviors
<!-- THEME_ID: T04 -->
This theme captures the shifting landscape of user preferences, moving beyond traditional passwords toward alternative authentication methods and addressing the social reality of credential sharing. There is a strong, articulated desire among participants to replace knowledge-based authentication with possession or inherence factors, such as biometrics and hardware tokens, which are perceived as both more secure and convenient. Furthermore, the data reveals that password management is not always a solitary activity; users frequently need to share access. This leads to a divergence in behavior: while some utilize dedicated features like family vaults, others resort to insecure methods like messaging apps, highlighting a gap between user needs and the availability or adoption of secure sharing tools.


- **CC_004**: A strong desire to replace...
  - _"反正现在都能手机号登录，密码基本也就是个摆设。"_ (P01)
  <!-- CODE_ID: CC_004 -->

- **CC_008**: The practice of sharing account...
  - _"视频会员经常借给朋友。我就直接微信发过去呗。"_ (P01)
  <!-- CODE_ID: CC_008 -->

- **CC_013**: A specific preference for using...
  - _"只要支持 2FA 的我都开。特别是 Google Authenticator，比短信安全。"_ (P02)
  <!-- CODE_ID: CC_013 -->

- **CC_021**: The use of dedicated security...
  - _"我用 1Password 的家庭共享功能。把需要的条目放到共享保险库里"_ (P03)
  <!-- CODE_ID: CC_021 -->




---

## 使用说明

1. 修改 `###` 后的文字来调整主题名称
2. 将编码条目剪切/粘贴到其他主题下进行重新分类
3. 添加新的 `### 主题名` 来创建新主题
4. 完成后运行 `llm-ta report` 生成最终报告