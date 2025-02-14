"""CLI for updating images and other routine tasks."""
from __future__ import annotations

import json

import click

from rhelocator import __version__
from rhelocator import update_images


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """Quick test."""


@click.command()
@click.option("--region", help="AWS region to query (optional)", type=str)
def aws_hourly_images(region: str) -> None:
    """Dump AWS hourly images from a region in JSON format"""
    # Verify that the user provided a region.
    if not region:
        raise click.UsageError(
            "Provide a valid AWS region with --region, such as 'us-east-1'"
        )

    # Is this a valid region?
    valid_regions = update_images.get_aws_regions()
    if region not in valid_regions:
        message = f"{region} is not valid. Valid regions include: \n\n  "
        message += "\n  ".join(valid_regions)
        raise click.UsageError(message)

    images = update_images.get_aws_images(region)
    click.echo(json.dumps(images, indent=2))


@click.command()
def aws_regions() -> None:
    """Get all valid AWS regions."""
    regions = update_images.get_aws_regions()
    click.echo(json.dumps(regions, indent=2))


cli.add_command(aws_hourly_images)
cli.add_command(aws_regions)
