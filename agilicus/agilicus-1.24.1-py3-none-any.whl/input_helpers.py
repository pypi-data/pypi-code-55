from . import context


def get_org_from_input_or_ctx(ctx, org_id=None, **kwargs):
    if org_id is not None:
        return org_id

    token = context.get_token(ctx)
    return context.get_org_id(ctx, token)
