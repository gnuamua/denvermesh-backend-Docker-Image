FROM plone:5

ADD site.cfg /plone/instance/
ADD versions.cfg /plone/instance/
USER plone
RUN buildout -c site.cfg
USER root
RUN find /data  -not -user plone -exec chown plone:plone {} \+ \
 && find /plone -not -user plone -exec chown plone:plone {} \+
CMD ["start"]
